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

app = Flask(__name__)

CORS(app)

user_URL = "http://localhost:5000/user"
driver_assignment_URL = "http://localhost:5002/driver_assignment"
order_URL = "http://localhost:5001/order"


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

def updateOrder(order_id, delivery_id, delivery_status="Assigned To Driver"):
    order = invoke_http(order_URL + "/order/" + str(order_id), method='GET')
    order["delivery_id"] = delivery_id
    order["delivery_status"] = delivery_status
    order = invoke_http(order_URL + "/order/" + str(order_id), json=order, method='PUT')
    return order

def getUserInfo(user_id):
    user_information = invoke_http(user_URL + "/user/" + str(user_id), method='GET')
    print("user_information:", user_information)
    return user_information

def assignDriver(delivery_details):
    assigned_driver = invoke_http(driver_assignment_URL, json=delivery_details, method='POST')
    return assigned_driver


def processPlaceDeliveryRequest(delivery_request):
    #1 get the user info
    user_id = delivery_request["user_id"]
    user_information = getUserInfo(user_id)
    user_address = user_information["address"]



    #2 send the delivery details to driver assignment service
    delivery_time = delivery_request["delivery_time"]
    order_id = delivery_request["order_id"]
    user_id = delivery_request["user_id"]
    delivery_details = { 
        "delivery_time" : delivery_time, 
        "order_id" : order_id, 
        "user_address" : user_address
    };
    assigned_driver = assignDriver(delivery_details)

    

    #3 update the order
    order = updateOrder(order_id, assigned_driver["delivery_id"])



    if connection is None or not amqp_lib.is_connection_open(connection):
        print("attempting to connect to amqp")
        connectAMQP()
        

    
    
    #convert order dict to string
    notification_message = {
        "status": delivery_status,
        "email": user_information["email"],
        "delivery_time": delivery_time,
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





@app.route("/place_delivery_request", methods=['POST'])
def place_delivery_request():
# Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            delivery_request = request.get_json()
            print("\nReceived a delivery request in JSON:", delivery_request)


            result = processPlaceDeliveryRequest(delivery_request)
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
            # TODO: Uncomment once order microservice is ready
            # Update order with new status
            # order_id = update_delivery_status_request["order_id"]
            # updateOrder(delivery_id, order_id, delivery_status=delivery_status)
            print(delivery_status)
            notification_message = {
                "status": delivery_status,
                "delivery_id": delivery_id,
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
