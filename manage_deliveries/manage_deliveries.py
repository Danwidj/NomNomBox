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

KAFKA_BROKER_URL = "localhost:9092"
KAFKA_TOPIC = "driver-schedule-updates"
KAFKA_ADMIN_CLIENT = "flask-admin-client"

app = Flask(__name__)



CORS(app)

user_URL = "http://localhost:5000/user"
schedule_URL = "http://localhost:5002/schedule"
order_URL = "http://localhost:5001/order"
delivery_URL = "http://localhost:5003/delivery"
availability_URL = "https://personal-6fbyxkeb.outsystemscloud.com/DriverAPI_REST/rest/Driver/Addorupdate_availability"


# RabbitMQ
rabbit_host = "localhost"
rabbit_port = 5672
exchange_name = "notification_topic"
exchange_type = "topic"
connection = None
channel = None

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

def update_order(order_id, delivery_id, delivery_status="Assigned To Driver"):
    order = invoke_http(order_URL + "/order/" + str(order_id), method='GET')
    order["delivery_id"] = delivery_id
    order["delivery_status"] = delivery_status
    order = invoke_http(order_URL + "/order/" + str(order_id), json=order, method='PUT')
    return order

def get_user_info(user_id):
    user_information = invoke_http(user_URL + "/user/" + str(user_id), method='GET')
    print("user_information:", user_information)
    return user_information

def assign_driver(desired_timeslot_details):
    assigned_driver = invoke_http(schedule_URL, json=desired_timeslot_details, method='POST')
    return assigned_driver

def create_delivery(delivery_details):
    delivery = invoke_http(delivery_URL, json=delivery_details, method='POST')
    return delivery

def update_availability(availability_details):
    availability = invoke_http(availability_URL, json=availability_details, method='POST')
    return availability

def check_driver_delivery_assignment(driver_id):
    assignments = invoke_http(schedule_URL + "?driver_id=" + str(driver_id), method='GET')
    return assignments["data"]

def process_place_delivery_request(delivery_request):
    #1 get the user info
    user_id = delivery_request["user_id"]
    user_information = get_user_info(user_id)
    user_address = user_information["address"]



    #2 send the desired timeslot to schedule service
    # time to be in unix timestamp
    desired_delivery_time = delivery_request["delivery_time"]
    desired_delivery_time_request = { 
        "desired_time": desired_delivery_time,
    };

    assigned_driver_response = assign_driver(desired_delivery_time_request)
    if assigned_driver_response["code"] != 201:
        return assigned_driver_response
    assigned_driver_id = assigned_driver_response["data"]["driver_id"]

    #3 send to delivery service
    delivery_details = {
        "order_id": delivery_request["order_id"],
        "timeslot": desired_delivery_time,
        "location": user_address,
        "driver_id": assigned_driver_id,
    }
    delivery_response = create_delivery(delivery_details)
    if delivery_response["code"] != 201:
        return delivery_response


    #4 update the order
    delivery_id = delivery_response["data"]["id"]
    order_id = delivery_request["order_id"]
    order = update_order(order_id=order_id, delivery_id=delivery_id)



    if connection is None or not amqp_lib.is_connection_open(connection):
        print("attempting to connect to amqp")
        connectAMQP()
        

    
    # 5 inform notification via amqp
    # time is in unix timestamp    
    #convert order dict to string
    notification_message = {
        "status": delivery_status,
        "email": user_information["email"],
        "delivery_time": desired_delivery_time,
        "order_id": order_id,
        "name": user_information["Name"],
    }
    notification_message = json.dumps(notification_message)

    delivery_status = order["delivery_status"]
    if delivery_status == "Assigned To Driver":
        # Inform the notification microservice
        print("  Publish message with routing_key=delivery.assigned\n")
        channel.basic_publish(
            exchange=exchange_name,
            routing_key="delivery.assigned",
            body=notification_message,
            properties=pika.BasicProperties(delivery_mode=2),
        )
producer = None
def start_producer():
    global producer
    producer = KafkaProducer(
        bootstrap_servers='localhost:9092')
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
    dt = datetime.fromisoformat(timestamp)
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
            driver_id = delivery_request["driver_id"]
            # delivery_assignments = check_driver_delivery_assignment(driver_id)
            timeslot_changes = delivery_request["changes"]
            occupied_timeslots= []
            for change in timeslot_changes:
                if change["change_type"] == "remove":
                    occupied_timeslots.append(change["timeslot"])
                    # for assignment in delivery_assignments:
                    # assigned_timeslot = convert_to_unix(assignment["timeslot"])
                    # if change["timeslot"] == assigned_timeslot or change["timeslot"] == assigned_timeslot + 1800:
                    #     occupied_timeslots.append(change["timeslot"])
            producer.send(KAFKA_TOPIC, value=json.dumps(delivery_request).encode())

            if len(occupied_timeslots) > 0:
                return jsonify({
                    "code": 200,
                    "message": "Request to modify timeslots pending. The system is checking if there are available drivers that can be re-assigned",
                }), 200
            else:
                result = update_availability(delivery_request)
                return jsonify(result), result["code"]



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


@app.route("/place_delivery_request", methods=['POST'])
def place_delivery_request():
# Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            delivery_request = request.get_json()
            print("\nReceived a delivery request in JSON:", delivery_request)


            result = process_place_delivery_request(delivery_request)
            return jsonify(result), result["code"]

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

    
@app.route("/update_delivery_status", methods=['POST'])
def update_delivery_request():
    if connection is None or not amqp_lib.is_connection_open(connection):
        print("attempting to connect to amqp")
        connectAMQP()
    # Structure of JSON request expected:
    # {
    #     "delivery_id": 1,
    #     "delivery_status": "Picked up by Driver"
    # }
    if request.is_json:
        try:
            update_delivery_status_request = request.get_json()
            delivery_id = update_delivery_status_request["delivery_id"]
            delivery_status = update_delivery_status_request["delivery_status"]
            delivery_time = update_delivery_status_request["delivery_time"]
            email = update_delivery_status_request["email"]
            name = update_delivery_status_request["name"]
            # TODO: Uncomment once order microservice is ready
            # Update order with new status
            # order_id = update_delivery_status_request["order_id"]
            # update_order(delivery_id, order_id, delivery_status=delivery_status)
            print(delivery_status)
            notification_message = {
                "status": delivery_status,
                "delivery_id": delivery_id,
                "email": email,
                "name": name,
                "delivery_time": delivery_time,
            }
            notification_message = json.dumps(notification_message)
            # publish messagae to exchange for notification service

            if delivery_status == "Picked up by Driver":
                print("  Publish message with routing_key=delivery.pickedup\n")
                
                channel.basic_publish(
                    exchange=exchange_name,
                    routing_key="delivery.pickedup",
                    body=notification_message,
                    properties=pika.BasicProperties(delivery_mode=2),
                )
            elif delivery_status == "Delivered by Driver":
                print("  Publish message with routing_key=delivery.delivered\n")
                channel.basic_publish(
                    exchange=exchange_name,
                    routing_key="delivery.delivered",
                    body=notification_message,
                    properties=pika.BasicProperties(delivery_mode=2),
                )

            elif delivery_status == "Received by Customer":
                print("  Publish message with routing_key=delivery.received\n")
                channel.basic_publish(
                    exchange=exchange_name,
                    routing_key="delivery.received",
                    body=notification_message,
                    properties=pika.BasicProperties(delivery_mode=2),
                )

        #TODO: update order status in database
            return {
                "code": 200,
                "message": "Delivery status updated"
            }



            
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
