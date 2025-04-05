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
    if method.routing_key == "delivery_cancellation.escalated":
        # Handle the escalation message
        logging.info("Received escalation message:", body.decode())
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

        # Acknowledge the message
        ch.basic_ack(delivery_tag=method.delivery_tag)

    elif method.routing_key == "delivery_cancellation.success":
        # 1 update old delivery with status of cancelled
        logging.info("Received success message:", body.decode())
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

        
        
        ch.basic_ack(delivery_tag=method.delivery_tag)





def start_consuming():
    # Start consuming messages from the RabbitMQ queue
    amqp_lib.start_consuming(
        hostname="rabbitmq",
        port=5672,
        exchange_name="delivery_cancellation_topic",
        exchange_type="topic",
        queue_name="delivery_cancellation_queue",
        callback=deal_with_delivery_status_change)

consumer_thread = threading.Thread(target=start_consuming)
consumer_thread.daemon = True  
consumer_thread.start()
def process_place_delivery_request(delivery_request):
    try:
        #1 get the user info
        auth_header = request.headers.get('Authorization')  # Get the Authorization header
        if not auth_header:
            return {"error": "Missing Authorization header"}, 401
        try:
            token = auth_header.split("Bearer ")[1]  # Extract token
        except IndexError:
            return {"error": "Invalid Authorization header format"}, 401
        
        user_id = delivery_request["user_id"]
        user_information = get_customer_info(user_id, token)
        if user_information["code"] not in range(200, 202):
            return jsonify({
                "code": 500,
                "message": "Failed to get user information",
                "error": user_information
            }), 500
        
        user_address = user_information["data"]["address"]

    
        #2 send the desired timeslot to schedule service
        # time to be in unix timestamp
        desired_delivery_time = delivery_request["delivery_time"]
        desired_delivery_time_request = { 
            "desired_timeslot": desired_delivery_time,
        }

        assigned_driver_response = assign_driver(desired_delivery_time_request)
        if assigned_driver_response["code"] not in range(200, 202):
            return jsonify({
                "code": 500,
                "message": "Failed to assign driver",
                "error": assigned_driver_response
            }), 500
        assigned_driver_id = assigned_driver_response["data"]["driver_id"]

        #3 send to delivery service
        delivery_details = {
            "order_id": delivery_request["order_id"],
            "timeslot": desired_delivery_time,
            "location": user_address,
            "driver_id": assigned_driver_id,
        }
        delivery_response = create_delivery(delivery_details)
        if delivery_response["code"] not in range(200, 202):
            return jsonify({
                "code": 500,
                "message": "Failed to create delivery",
                "error": delivery_response
            }), 500


        #4 update the order
        delivery_id = delivery_response["data"]["id"]
        order_id = delivery_request["order_id"]
        order = update_order(order_id=order_id, delivery_id=delivery_id)
        if order["code"] not in range(200, 202):
            return jsonify({
                "code": 500,
                "message": "Failed to update order",
                "error": order
            }), 500
        

        if RabbitMQManager.connection is None or not amqp_lib.is_connection_open(RabbitMQManager.connection):
            logging.info("attempting to connect to amqp")
            RabbitMQManager.start(rabbit_host, rabbit_port, exchange_name, exchange_type)
            

        
        # 5 inform notification via amqp
        # time is in unix timestamp    
        #convert order dict to string
        notification_message = {
            "status": "Assigned to Driver",
            "email": user_information["data"]["email"],
            "delivery_time": desired_delivery_time,
            "order_id": order_id,
            "name": user_information["data"]["name"],
            "delivery_id": delivery_id,
        }
        notification_message = json.dumps(notification_message)


        # Inform the notification microservice
        logging.info("  Publish message with routing_key=delivery.assigned\n")
        RabbitMQManager.channel.basic_publish(
            exchange=exchange_name,
            routing_key="delivery.assigned",
            body=notification_message,
            properties=pika.BasicProperties(delivery_mode=2),
        )
        return jsonify({
            "code": 200,
            "message": "Delivery request placed successfully",
            "data": {   
                "deliveryId" : delivery_id,
                "driverId" : assigned_driver_id,
            }
        }), 200
    
    except Exception as e:
        error_details = traceback.format_exc()
        logging.error("Exception occurred while processing delivery request:\n%s", error_details)
        return jsonify({
            "code": 500,
            "message": "Internal server error: " + str(e),
            "error_details": error_details
        }), 500
    




@app.route("/message", methods=['POST'])
def post_message():
    try:
        if KafkaManager.producer is None:
            KafkaManager.start_producer()
        # Get the message from the request
        message = request.json
        message = json.dumps(message).encode()
        
        if not message:
            return jsonify({"error": "Invalid message format"}), 400

        KafkaManager.producer.send(KAFKA_TOPIC, value=message)

        # Return success response
        return jsonify({"message": "Message sent"}), 200
    except Exception as e:
        # Handle any errors
        return jsonify({"error": str(e)}), 500



@app.route("/availability", methods=["POST"])
def update_availability():
    try:
        if KafkaManager.producer is None:
            KafkaManager.start_producer()
    except Exception as e:
        # Handle any errors
        return jsonify({"error": str(e)}), 500
        
# Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            delivery_request = request.get_json()
            print("\nReceived a update availability request in JSON:", delivery_request)
            # first check if driver has already been assigned to any deliveries if he wants to remove timeslot
            # driver_id = delivery_request["driver_id"]
            # delivery_assignments = check_driver_delivery_assignment(driver_id)
            timeslot_changes = delivery_request["changes"]
            occupied_timeslots= []
            for change in timeslot_changes:
                if change["change_type"] == "delete":
                    occupied_timeslots.append(change["timeslot"])
                    # for assignment in delivery_assignments:
                    # assigned_timeslot = convert_to_unix(assignment["timeslot"])
                    # if change["timeslot"] == assigned_timeslot or change["timeslot"] == assigned_timeslot + 1800:
                    #     occupied_timeslots.append(change["timeslot"])
            
            occupied_timeslots = [t for timeslot in occupied_timeslots for t in (timeslot, timeslot + 30 * 60)]

            if len(occupied_timeslots) > 0:
                # check if the driver is already assigned to any deliveries in the occupied timeslots
                # if so, return error
                response = requests.get("http://127.0.0.1:5000/deliveries?driver_id=" + str(delivery_request["driver_id"]))
                if response.status_code != 200:
                    return jsonify({
                        "code": response.status_code,
                        "message": "Failed to get deliveries",
                        "error": response.json()
                    }), response.status_code
                else:
                    deliveries = response.json()["data"]
                    for delivery in deliveries:
                        if delivery["timeslot"] in occupied_timeslots and delivery["status"] != "Received by Customer" and delivery["status"] != "Cancelled":
                            return jsonify({
                                "code": 400,
                                "message": "Driver is already assigned to a delivery in the occupied timeslot",
                            }), 400
                    
                
                result = update_driver_availability(delivery_request)
                if result.status_code != 200:
                    return jsonify({
                        "code": result.status_code,
                        "message": "Failed to update availability",
                        "error": result.json()
                    }), result.status_code
                else:
                    KafkaManager.producer.send(KAFKA_TOPIC, value=json.dumps(delivery_request).encode())
                    return jsonify({
                        "code": result.status_code,
                        "results": result.json()["results"],
                    }), result.status_code

            else:
                result = update_driver_availability(delivery_request)
                if result.status_code != 200:
                    return jsonify({
                        "code": result.status_code,
                        "message": "Failed to update availability",
                        "error": result.json()
                    }), result.status_code
                else:
                    KafkaManager.producer.send(KAFKA_TOPIC, value=json.dumps(delivery_request).encode())
                    return jsonify({
                        "code": result.status_code,
                        "results": result.json()["results"],
                    }), result.status_code
                




        except Exception as e:

            logging.error("Exception occurred while updating availability:\n%s", traceback.format_exc())


            return jsonify({
                "code": 500,
                "message": "Internal server error: " + str(e)
            }), 500


    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400


@app.route("/place_delivery_request", methods=['POST'])
def place_delivery_request():
# Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            delivery_request = request.get_json()
            print("\nReceived a delivery request in JSON:", delivery_request)


            result = process_place_delivery_request(delivery_request)
            return result

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "place_delivery_request.py internal error: " + ex_str
            }), 500


    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400


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
                    properties=pika.BasicProperties(delivery_mode=2, expiration="10"),
                )
                return jsonify({
                    "code": 200,
                    "message": "Delivery status updated to pending cancellation"
                }), 200

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


# interface Delivery {
#   id: string;
#   delivery_id: string;
#   driver_id: string;
#   timeslot: number; // Unix timestamp
#   location: string;
#   status: DeliveryStatus;
# }
@app.route("/deliveries", methods=['GET'])
def get_assigned_deliveries():
    response=[]
    order_ids = { "order_ids": [] }
    try:
    # 1. Get deliveries by driver id
        driver_id = request.args.get('driver_id')
        if driver_id:
            deliveries = get_deliveries_by_driver_id(driver_id)
            # deliveries = jsonify(deliveries)
            logging.info(f"deliveries:\n{json.dumps(deliveries, indent=4)}")
            for delivery in deliveries:
                response.append({
                    "delivery_id": delivery["id"],
                    "timeslot": delivery["timeslot"],
                    "location": delivery["location"],
                    "order_id": delivery["order_id"],
                })
                order_ids["order_ids"].append(delivery["order_id"])

        else:
            return jsonify({
                "code": 400,
                "message": "Invalid request"
            }), 400
        # orders=[]
    # 2. Get status from order for the delivery
    
        logging.info(f"response from deliveries: {response}")
        orders = get_orders(order_ids)
        orders = orders["data"]
        # dk if there is error in this filtering logic
        for i in range(len(response)):
            if "error" in orders[i].keys():
                pass

            else:
                if response[i]["cancellation_status"] is not None:
                    response[i]["status"] = response[i]["cancellation_status"]
                else:                
                    response[i]["status"] = orders[i]["data"]["status"]
            
            # orders.append(order)
            # if order["code"] == 404:
            #     return jsonify({
            #         "code": 404,
            #         "message": "Order not found"
            #     }), 404
            # print("order:", order)
            # delivery["status"] = order["status"]  
        pretty_json = json.dumps(orders, indent=4)
        logging.info(f"response from orders: {pretty_json}")
        return jsonify({
            "code":200,
            "data": response
        }), 200
    except Exception as e:
        
        logging.error("Error:", str(e))
        logging.error(traceback.format_exc())
        
        return jsonify({
            "code": 500,
            "message": "Internal server error: " + str(e)
        }), 500



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
