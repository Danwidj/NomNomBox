import logging
import traceback
import requests
import json
import pika
from flask import request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore, auth
from invokes import invoke_http
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

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

KAFKA_BROKER_URL = "kafka:9092"
KAFKA_TOPIC = "driver-schedule-updates"
KAFKA_ADMIN_CLIENT = "flask-admin-client"

db = firestore.client()
user_URL = "http://customer:5002"
schedule_URL = "http://schedule:5001"
order_URL = "http://order:5003"
delivery_URL = "http://delivery:5000"
driver_availability_URL = "https://personal-6fbyxkeb.outsystemscloud.com/Driver/rest/DriverAPI/drivers/timeslots/"

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
    if deliveries["code"] not in range(200, 300):
        return deliveries
    deliveries = deliveries["data"]["deliveries"]
    for delivery in deliveries:
        delivery["timeslot"] = convert_to_unix(delivery["timeslot"])
    return { "code": 200, "data": { "deliveries": deliveries }}

def get_orders(order_ids):
    order = invoke_http(order_URL + "/api/orders", json=order_ids, method='POST')
    return order

def get_order_by_id(order_id):
    order = invoke_http(order_URL + "/api/orders/" + str(order_id), method='GET')
    return order

def convert_to_unix(timestamp: str) -> int:
    # Define the format that matches the 'Sat, 08 Mar 2025 11:00:00 GMT' timestamp
    timestamp_format = "%a, %d %b %Y %H:%M:%S GMT"
    
    # Parse the timestamp using the defined format
    dt = datetime.strptime(timestamp, timestamp_format)
    
    # Return the Unix timestamp
    return int(dt.timestamp())



