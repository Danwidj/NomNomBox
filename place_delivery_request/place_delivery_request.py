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
        
        # 5 get driver information
        driver_response = requests.get(driver_URL + str(assigned_driver_id) + "/info")
        if driver_response.status_code not in range(200, 202):
            return jsonify({
                "code": 500,
                "message": "Failed to get driver information",
                "error": driver_response.json()
            }), 500
        
        driver_response = driver_response.json()
        


        if RabbitMQManager.connection is None or not amqp_lib.is_connection_open(RabbitMQManager.connection):
            logging.info("attempting to connect to amqp")
            RabbitMQManager.start(rabbit_host, rabbit_port, exchange_name, exchange_type)
        

        driver_notification_message = {
            "delivery_id": delivery_id,
            "name": driver_response["name"],
            "email": driver_response["email"],
            "location": user_address,
            "timeslot": desired_delivery_time,
            "status": "Assigned to Driver",
        }
        driver_notification_message = json.dumps(driver_notification_message)
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
            body=driver_notification_message,
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
    



@app.route("/", methods=['POST'])
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
            logging.info(f"deliveries:\n{json.dumps(deliveries, indent=4)}")
            if deliveries["code"] == 404:
                return jsonify({
                    "code": 404,
                    "message": "No deliveries found for this driver"
                }), 404
            elif deliveries["code"] not in range(200, 202):
                return jsonify({
                    "code": 500,
                    "message": "Failed to get deliveries",
                    "error": deliveries
                }), 500
            deliveries = deliveries["data"]["deliveries"]
            # deliveries = jsonify(deliveries)
            for delivery in deliveries:
                response.append({
                    "delivery_id": delivery["id"],
                    "timeslot": delivery["timeslot"],
                    "location": delivery["location"],
                    "order_id": delivery["order_id"],
                    "cancellation_status": delivery["cancellation_status"],
                })
                order_ids["order_ids"].append(delivery["order_id"])

        else:
            return jsonify({
                "code": 400,
                "message": "Invalid request"
            }), 400
        # orders=[]
    # 2. Get status from order for the delivery
    
        # logging.info(f"response from deliveries: {response}")
        orders = get_orders(order_ids)
        orders = orders["data"]
        # dk if there is error in this filtering logic
        # for i in range(len(response)):
        #     if "error" in orders[i].keys():
        #         pass

        #     else:
        #         if response[i]["cancellation_status"] is not None:
        #             response[i]["status"] = response[i]["cancellation_status"]
        #         else:                
        #             response[i]["status"] = orders[i]["data"]["status"]
        
        
        orders = get_orders(order_ids)
        orders = orders["data"]

       
        orders_by_id = {order["order_id"]: order for order in orders}

        new_response = []

        for item in response:
            order_id = item["order_id"]
            order = orders_by_id.get(order_id)

            if not order or "error" in order:
                continue

            if item["cancellation_status"] is not None:
                item["status"] = item["cancellation_status"]
            else:
                item["status"] = order["data"]["status"]

            new_response.append(item)

        response = new_response

            
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
        
        logging.error(f"Error: {str(e)}")
        logging.error(traceback.format_exc())
        
        return jsonify({
            "code": 500,
            "message": "Internal server error: " + str(e)
        }), 500





if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5014, debug=True)