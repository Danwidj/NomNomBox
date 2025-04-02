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
from contextlib import asynccontextmanager
import asyncio
import traceback
import requests
import logging
import firebase_admin
from firebase_admin import credentials, firestore, auth
import time
# KAFKA_BROKER_URL = "localhost:9092"
KAFKA_BROKER_URL = "kafka:9092"
KAFKA_TOPIC = "driver-schedule-updates"
KAFKA_ADMIN_CLIENT = "flask-admin-client"


load_dotenv()

# Get Firebase credentials
firebase_credentials_path = os.getenv("FIREBASE_CREDENTIALS")
firebase_api_key = os.getenv("FIREBASE_API_KEY")  # Required for REST API authentication

if not firebase_credentials_path:
    raise ValueError("Missing FIREBASE_CREDENTIALS in .env file")

# Initialize Firebase if not already initialized
if not firebase_admin._apps:
    try:
        cred = credentials.Certificate(firebase_credentials_path)
        firebase_admin.initialize_app(cred)
    except Exception as e:
        raise RuntimeError(f"Failed to initialize Firebase: {e}")

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
connection = None
channel = None

# firebase_api_key = os.getenv("FIREBASE_API_KEY")
email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")
# logging.info("Firebase API Key: %s", firebase_api_key)
logging.basicConfig(level=logging.INFO)

def connectAMQP():
    # Use global variables to reduce number of reconnection to RabbitMQ
    # There are better ways but this suffices for our lab
    global connection
    global channel

    print("  Connecting to AMQP broker...")
    try:
        connection, channel = amqp_lib.connect(
                hostname=rabbit_host,
                port=rabbit_port,
                exchange_name=exchange_name,
                exchange_type=exchange_type,
        )
    except Exception as exception:
        print(f"  Unable to connect to RabbitMQ.\n     {exception=}\n")
        exit(1) # terminate

def update_order(order_id, delivery_id, status="Assigned To Driver"):
    try: 
        order = {}
        order["deliveryId"] = delivery_id
        order["status"] = status
        order_response = invoke_http(order_URL + "/api/orders/" + str(order_id), json=order, method='PATCH')
        return order_response
    except Exception as e:
        logging.error("Exception occurred while updating order:\n%s", traceback.format_exc())

def get_customer_info(customer_id, token):
    headers = {
        "Authorization": f"Bearer {token}",
    }
    try:
        # dk why checking for status code does not work
        response = requests.get(user_URL + "/customer/" + str(customer_id), headers=headers)
        response.raise_for_status()
        # if response.status_code != 200:
        #     return {
        #         "code": response.status_code,
        #         "message": "Failed to get user information",
        #         "error": response.json()
        #     }
        user_information = response.json()
        return user_information
    except requests.exceptions.HTTPError as http_err:
        # If the request failed due to HTTP error (e.g., 404 or 500)
        return {
            "code": response.status_code,
            "message": f"HTTP error occurred: {http_err}",
            "error": response.text
        }

    except requests.exceptions.RequestException as req_err:
        # If there was a network problem or any other error
        return {
            "code": 500,
            "message": f"Request error occurred: {req_err}",
            "error": str(req_err)
        }



def assign_driver(desired_timeslot_details):
    assigned_driver = invoke_http(schedule_URL + "/schedule", json=desired_timeslot_details, method='POST')
    return assigned_driver

def create_delivery(delivery_details):
    delivery = invoke_http(delivery_URL + "/delivery", json=delivery_details, method='POST')
    return delivery

def update_driver_availability(availability_details):
    availability = requests.post(driver_availability_URL, json=availability_details)
    # availability = invoke_http(driver_availability_URL, json=availability_details, method='POST')
    return availability

def check_driver_delivery_assignment(driver_id):
    assignments = invoke_http(schedule_URL + "?driver_id=" + str(driver_id), method='GET')
    return assignments

def get_deliveries_by_driver_id(driver_id):
    deliveries = invoke_http(delivery_URL + "/delivery?driver_id=" + str(driver_id), method='GET')
    deliveries = deliveries["data"]["deliveries"]
    for delivery in deliveries:
        delivery["timeslot"] = convert_to_unix(delivery["timeslot"])
    return deliveries

def get_orders(order_ids):
    order = invoke_http(order_URL + "/api/orders", json=order_ids, method='POST')
    return order

def get_order_by_id(order_id):
    order = invoke_http(order_URL + "/api/orders/" + str(order_id), method='GET')
    return order





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
        




        if connection is None or not amqp_lib.is_connection_open(connection):
            logging.info("attempting to connect to amqp")
            connectAMQP()
            

        
        # 5 inform notification via amqp
        # time is in unix timestamp    
        #convert order dict to string
        notification_message = {
            "status": "Assigned to Driver",
            "email": user_information["data"]["email"],
            "delivery_time": desired_delivery_time,
            "order_id": order_id,
            "name": user_information["data"]["name"],
        }
        notification_message = json.dumps(notification_message)


        # Inform the notification microservice
        logging.info("  Publish message with routing_key=delivery.assigned\n")
        channel.basic_publish(
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

producer = None
def start_producer():
    global producer
    producer = KafkaProducer(
        bootstrap_servers='kafka:9092', api_version=(2, 6, 0))
    # Get cluster layout and initial topic/partition leadership information
    print("producer abt to start")
    # producer.start()
    # print("producer started")



def publish_message(message):
    global producer
    try:
        if producer is None:
            start_producer()
        # Get the message from the request
        message = request.json
        message = json.dumps(message).encode()
        
        if not message:
            return jsonify({"error": "Invalid message format"}), 400

        producer.send(KAFKA_TOPIC, value=message)

        # Return success response
        return jsonify({"message": "Message sent"}), 200
    except Exception as e:
        # Handle any errors
        return jsonify({"error": str(e)}), 500


@app.route("/message", methods=['POST'])
def post_message():
    global producer
    try:
        if producer is None:
            start_producer()
        # Get the message from the request
        message = request.json
        message = json.dumps(message).encode()
        
        if not message:
            return jsonify({"error": "Invalid message format"}), 400

        producer.send(KAFKA_TOPIC, value=message)

        # Return success response
        return jsonify({"message": "Message sent"}), 200
    except Exception as e:
        # Handle any errors
        return jsonify({"error": str(e)}), 500

def convert_to_unix(timestamp: str) -> int:
    # Define the format that matches the 'Sat, 08 Mar 2025 11:00:00 GMT' timestamp
    timestamp_format = "%a, %d %b %Y %H:%M:%S GMT"
    
    # Parse the timestamp using the defined format
    dt = datetime.strptime(timestamp, timestamp_format)
    
    # Return the Unix timestamp
    return int(dt.timestamp())

@app.route("/availability", methods=["POST"])
def update_availability():
    global producer
    try:
        if producer is None:
            start_producer()
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
            producer.send(KAFKA_TOPIC, value=json.dumps(delivery_request).encode())
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
                        if delivery["timeslot"] in occupied_timeslots and delivery["status"] != "Received by Customer":
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
                    return jsonify({
                        "code": result.status_code,
                        "results": result.json()["results"],
                    }), result.status_code
                




        except Exception as e:
            # Unexpected error in code
            # exc_type, exc_obj, exc_tb = sys.exc_info()
            # fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            # ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            # print(ex_str)
            logging.error("Exception occurred while updating availability:\n%s", traceback.format_exc())

            # return jsonify({
            #     "code": 500,
            #     "message": "place_delivery_request.py internal error: " + ex_str
            # }), 500
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
    if connection is None or not amqp_lib.is_connection_open(connection):
        print("attempting to connect to amqp")
        connectAMQP()
    # Structure of JSON request expected:
    # {
    #     "order_id": 1,
    #     "status": "Picked up by Driver"
    # }
    if request.is_json:
        try:
            update_delivery_request = request.get_json()
            order_id = update_delivery_request["order_id"]
            status = update_delivery_request["status"]
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
            time.sleep(2)
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
                # "delivery_time": delivery_ytime,
            }
            notification_message = json.dumps(notification_message)
            
            # publish messagae to exchange for notification service

            if status == "Picked up by Driver":
                print("  Publish message with routing_key=delivery.pickedup\n")
                
                channel.basic_publish(
                    exchange=exchange_name,
                    routing_key="delivery.pickedup",
                    body=notification_message,
                    properties=pika.BasicProperties(delivery_mode=2),
                )
            elif status == "Delivered by Driver":
                print("  Publish message with routing_key=delivery.delivered\n")
                channel.basic_publish(
                    exchange=exchange_name,
                    routing_key="delivery.delivered",
                    body=notification_message,
                    properties=pika.BasicProperties(delivery_mode=2),
                )

            elif status == "Received by Customer":
                print("  Publish message with routing_key=delivery.received\n")
                channel.basic_publish(
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
            logging.info(f"deliveries: {deliveries}")
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
                response[i]["status"] = orders[i]["data"]["status"]
            
            # orders.append(order)
            # if order["code"] == 404:
            #     return jsonify({
            #         "code": 404,
            #         "message": "Order not found"
            #     }), 404
            # print("order:", order)
            # delivery["status"] = order["status"]  
        logging.info(f"response from orders: {orders}")
        return jsonify({
            "code":200,
            "data": response
        }), 200
    except Exception as e:
        print("Error:", str(e))  # Print simple error message
        traceback.print_exc()  # Print full stack trace for debugging
        
        return jsonify({
            "code": 500,
            "message": "Internal server error: " + str(e)
        }), 500




    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
