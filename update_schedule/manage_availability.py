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



# firebase_api_key = os.getenv("FIREBASE_API_KEY")
# email = os.getenv("EMAIL")
# password = os.getenv("PASSWORD")
# logging.info("Firebase API Key: %s", firebase_api_key)
logging.basicConfig(level=logging.INFO)




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
                response = requests.get("http://place_delivery_request:5014/deliveries?driver_id=" + str(delivery_request["driver_id"]))
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5011, debug=True)