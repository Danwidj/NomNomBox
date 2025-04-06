from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv, dotenv_values
from datetime import datetime, timezone
from invokes import invoke_http
import amqp_lib
import json
import pika
import sys
from kafka import KafkaProducer
import traceback
import requests
import logging
import firebase_admin
from firebase_admin import credentials, firestore, auth
from helper_functions import get_deliveries_by_driver_id, get_orders, update_order, update_driver_availability, get_customer_info, get_order_by_id, create_delivery, assign_driver
import time
from RabbitMQManager import RabbitMQManager
from KafkaManager import KafkaManager
import threading
# KAFKA_BROKER_URL = "localhost:9092"
KAFKA_BROKER_URL = "kafka:9092"
KAFKA_TOPIC = "driver-schedule-updates"
KAFKA_ADMIN_CLIENT = "flask-admin-client"


load_dotenv()


app = Flask(__name__)
CORS(app)
db = firestore.client()
user_URL = "http://customer:5002"
schedule_URL = "http://schedule:5001"
order_URL = "http://order:5003"
delivery_URL = "http://delivery:5000"
driver_availability_URL = "https://personal-6fbyxkeb.outsystemscloud.com/Driver/rest/DriverAPI/drivers/timeslots/"
driver_URL = "https://personal-6fbyxkeb.outsystemscloud.com/DriverService/rest/v1/drivers/"


# RabbitMQ
# rabbit_host = "localhost"
rabbit_host = "rabbitmq"
rabbit_port = 5672
exchange_name = "notification_topic"
exchange_type = "topic"



firebase_api_key = os.getenv("FIREBASE_API_KEY")
email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")
# logging.info("Firebase API Key: %s", firebase_api_key)
logging.basicConfig(level=logging.INFO)



# Only subscribed to the main queue, and only acknowledge cancelled and esccalated messages
def deal_with_delivery_status_change(ch, method, properties, body):
    if RabbitMQManager.connection is None or not amqp_lib.is_connection_open(RabbitMQManager.connection):
        logging.info("attempting to connect to amqp")
        RabbitMQManager.start(rabbit_host, rabbit_port, exchange_name, exchange_type)
    with app.app_context():
        if method.routing_key == "delivery_cancellation.escalated":
            # Handle the escalation message
            logging.info("Received escalation message: %s", body.decode())
            # Parse the message
            message = json.loads(body.decode())
            delivery_id = message["delivery_id"]
            try:
                delivery_response = invoke_http(delivery_URL + "/delivery/" + str(delivery_id), json={ "cancellation_status": "Escalated"}, method='PATCH')
                
            except Exception as e:
                return jsonify({
                    "code": 500,
                    "message": "Failed to update delivery with pending cancellation status",
                    "error": str(e)
                }), 500

            
            ch.basic_ack(delivery_tag=method.delivery_tag)

        elif method.routing_key == "delivery_cancellation.success":
            # 1 update old delivery with status of cancelled
            logging.info("Received success message: %s", body.decode())
            # Parse the message
            message = json.loads(body.decode())
            delivery_id = message["delivery_id"]
            try:
                delivery_response = invoke_http(delivery_URL + "/delivery/" + str(delivery_id), json={ "cancellation_status": "Cancelled"}, method='PATCH')
            except Exception as e:
                logging.error(traceback.format_exc())
            if delivery_response["code"] not in range(200, 202):
                logging.error("Failed to update delivery with cancelled status: %s", delivery_response)


            # 2 create new delivery with new driver id 
            new_delivery_details = {
                "driver_id" : message["reassigned_driver_id"],
                "location" : message["location"],
                "order_id" : message["order_id"],
                "timeslot" : message["timeslot"],
            }
            try:
                new_delivery_response = create_delivery(new_delivery_details)
            except Exception as e:
                logging.error(traceback.format_exc())
            if new_delivery_response["code"] not in range(200, 202):
                logging.error("Failed to create new delivery: %s", new_delivery_response)


            # 3 update order with new delivery id
            order_id = message["order_id"]
            new_delivery_id = new_delivery_response["data"]["id"]
            try:
                order_response = update_order(order_id=order_id, delivery_id=new_delivery_id)
            except Exception as e:
                logging.error(traceback.format_exc())
            if order_response["code"] not in range(200, 202):
                logging.error("Failed to update order with new delivery id: %s", order_response)
            # 4 send notification message to old driver
            #TODO

            
            
            # RabbitMQManager.channel.basic_publish(
            #     exchange=exchange_name,
            #     routing_key="delivery.cancelled",
            #     body=notification_message,
            #     properties=pika.BasicProperties(delivery_mode=2),
            # )

            # get driver information
            driver_response = requests.get(driver_URL + str(message["reassigned_driver_id"]) + "/info")
            if driver_response.status_code not in range(200, 202):
                logging.error("Failed to get driver information: %s", driver_response.json())
            driver_response = driver_response.json()

            # 5 send notification message to new driver
            notification_message = {
                "status": "Assigned to Driver",
                "email": driver_response["email"],
                "timeslot": message["timeslot"],
                "name": driver_response["name"],
                "delivery_id": delivery_id,
                "location": message["location"],
            }
            notification_message = json.dumps(notification_message)
            RabbitMQManager.channel.basic_publish(
                exchange=exchange_name,
                routing_key="delivery.assigned",
                body=notification_message,
                properties=pika.BasicProperties(delivery_mode=2),
            )



            ch.basic_ack(delivery_tag=method.delivery_tag)

            
        else:    
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)





def start_consuming():
    # Start consuming messages from the RabbitMQ queue

    amqp_lib.start_consuming(
        hostname="rabbitmq",
        port=5672,
        exchange_name="delivery_cancellation_topic",
        exchange_type="topic",
        queue_name="delivery_cancellation_general_queue",
        callback=deal_with_delivery_status_change)




consumer_thread = threading.Thread(target=start_consuming)
consumer_thread.daemon = True  
consumer_thread.start()



@app.route("/deliveries/<int:delivery_id>", methods=['PATCH'])
def update_delivery_status(delivery_id):
    if RabbitMQManager.connection is None or not amqp_lib.is_connection_open(RabbitMQManager.connection):
        print("attempting to connect to amqp")
        RabbitMQManager.start(rabbit_host, rabbit_port, exchange_name, exchange_type)
    # Structure of JSON request expected:
    # {
    #     "order_id": 1,
    #     "status": "Picked up by Driver"
    #     "timeslot": 1234567890
    # }
    if request.is_json:
        try:
            update_delivery_request = request.get_json()
            order_id = update_delivery_request["order_id"]
            status = update_delivery_request["status"]
            timeslot = update_delivery_request["timeslot"]
            
            # business exception: driver cancels delivery
            if status == "Pending Cancellation":                
                # update delivery with delivery exclusive status (all the cancellation related stuff)
                #request to patch delivery with Pending Cancellation status
                try:
                    delivery_response = invoke_http(delivery_URL + "/delivery/" + str(delivery_id), json={ "cancellation_status": "Pending Cancellation"}, method='PATCH')
                except Exception as e:
                    return jsonify({
                        "code": 500,
                        "message": "Failed to update delivery with pending cancellation status",
                        "error": str(e)
                    }), 500

                RabbitMQManager.channel.basic_publish(
                    exchange="delivery_cancellation_topic",
                    routing_key="delivery_cancellation.pending",
                    body=json.dumps(update_delivery_request),
                    properties=pika.BasicProperties(delivery_mode=2, expiration="0"),
                )
                return jsonify({
                    "code": 200,
                    "message": "Delivery status updated to pending cancellation"
                }), 200
            #  if other statuses...
            # update order with new status
            update_response = update_order(order_id=order_id, delivery_id=delivery_id, status=status)
            logging.info("update_response: %s", update_response)
            if update_response["code"] == 404:
                return jsonify({
                    "code": 404,
                    "message": "Order not found"
                }), 404
            elif update_response["code"] not in range(200, 202):
                return jsonify({
                    "code": 500,
                    "message": "Failed to update order",
                    "error": update_response
                }), 500
            # get order by id to get customer id
            order = get_order_by_id(order_id)
            customer_id = order["data"]["customerId"]
            # get token from firebase
            firebase_auth_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={firebase_api_key}"
            payload = {"email": email, "password": password, "returnSecureToken": True}
            response = requests.post(firebase_auth_url, json=payload)
            if response.status_code == 200:
                auth_data = response.json()
                token = auth_data["idToken"]
            else:
                return jsonify({"code": 401, "message": "Invalid credentials while connecting to firebase for auth token", "error": response.json()}), 401
            
            # use token from firebase to coneect to customer service to  get customer info
            time.sleep(1)
            customer_info = requests.get(user_URL + "/customer/" + str(customer_id), headers={"Authorization": f"Bearer {token}"})
            if customer_info.status_code == 404:
                return jsonify({
                    "code": 404,
                    "message": "Customer not found"
                }), 404
            elif customer_info.status_code != 200:
                return jsonify({
                    "code": 500,
                    "message": "Failed to get customer information",
                    "error": customer_info.json()
                }), 500
            customer_info = customer_info.json()

            logging.info("customer_info: %s", customer_info)
            notification_message = {
                "status": status,
                "delivery_id": delivery_id,
                "email": customer_info["data"]["email"],
                "name": customer_info["data"]["name"],
                "order_id": order_id,
            }
            notification_message = json.dumps(notification_message)
            
            # publish messagae to exchange for notification service

            if status == "Picked up by Driver":
                print("  Publish message with routing_key=delivery.pickedup\n")
                
                RabbitMQManager.channel.basic_publish(
                    exchange=exchange_name,
                    routing_key="delivery.pickedup",
                    body=notification_message,
                    properties=pika.BasicProperties(delivery_mode=2),
                )
            elif status == "Delivered by Driver":
                print("  Publish message with routing_key=delivery.delivered\n")
                RabbitMQManager.channel.basic_publish(
                    exchange=exchange_name,
                    routing_key="delivery.delivered",
                    body=notification_message,
                    properties=pika.BasicProperties(delivery_mode=2),
                )

            elif status == "Received by Customer":
                print("  Publish message with routing_key=delivery.received\n")
                RabbitMQManager.channel.basic_publish(
                    exchange=exchange_name,
                    routing_key="delivery.received",
                    body=notification_message,
                    properties=pika.BasicProperties(delivery_mode=2),
                )


            return {
                "code": 200,
                "message": "Delivery status updated"
            }

            
        except Exception as e:
            # Unexpected error in code
            logging.error("Exception occurred while updating delivery status:\n%s", traceback.format_exc())


            return jsonify({
                "code": 500,
                "message": str(e)
            }), 500



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5013, debug=True)
