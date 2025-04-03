from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv, dotenv_values
from datetime import datetime, timezone
import random
import json
import threading
import time
from kafka import KafkaConsumer
from datetime import timedelta
import traceback
import redis_utils 
import logging
from KafkaManager import KafkaManager

app = Flask(__name__)
app.logger.setLevel(logging.INFO)

CORS(app)
load_dotenv(".env")
print(os.getenv("DATABASE_HOST"))

app.config["SQLALCHEMY_DATABASE_URI"] = (
     os.getenv("DATABASE_HOST")
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

KAFKA_BROKER_URL = "kafka:9092"
KAFKA_TOPIC = "driver-schedule-updates"

messages = []
logging.basicConfig(level=logging.INFO)
class Schedule(db.Model):
    __tablename__ = "schedule"


    id = db.Column(db.Integer, primary_key=True)
    timeslot = db.Column(db.TIMESTAMP(timezone=True), nullable=False)
    driver_id = db.Column(db.Integer, nullable=False)
    assigned = db.Column(db.Boolean, nullable=False)



    def __init__(self, timeslot, driver_id, assigned):
        self.timeslot = timeslot
        self.driver_id = driver_id
        self.assigned = assigned


    def json(self):
        return {
            "id": self.id,
            "driver_id": self.driver_id,
            "timeslot": int(self.timeslot.timestamp()),
            "assigned": self.assigned
        }

def consume(consumer):
    try:
        for msg in consumer:
            decoded_message = msg.value.decode('utf-8')
            print(f"Received: {decoded_message}")  # Log message
            logging.info(f"Received: {decoded_message}")  # Log message
            messages.append(json.loads(decoded_message))  # Store message in memory
            received_event = json.loads(decoded_message)
            schedule_change = received_event["changes"]
            driver_id = received_event["driver_id"]
            with app.app_context():
                for change in schedule_change:
                    time_slot = datetime.fromtimestamp(int(change["timeslot"]), timezone.utc)
                    # print (start_time, end_time)
                    counter_time = time_slot
                    if change["change_type"] == "add":
                        while counter_time < time_slot + timedelta(minutes=60):
                            new_schedule = Schedule(
                                timeslot=counter_time,
                                driver_id=driver_id,
                                assigned=False
                            )
                            db.session.add(new_schedule)
                            counter_time += timedelta(minutes=30)


                    elif change["change_type"] == "delete":
                        while counter_time < time_slot + timedelta(minutes=60):
                            db.session.query(Schedule).filter(Schedule.timeslot == counter_time, Schedule.driver_id == driver_id).delete()
                            counter_time += timedelta(minutes=30)
                            # print(counter_time)
        
                print("committed")
                db.session.commit()
        # print(f"Messages: {messages}")
            
    except Exception as e:
        error_trace = traceback.format_exc()
        logging.exception(f"Error consuming messages: {e} \n {error_trace}")
    
    finally:
        consumer.close()
        print("Consumer closed")

KafkaManager.start_kafka_consumer(KAFKA_TOPIC, KAFKA_BROKER_URL)

def consuming():
    while True:
        if KafkaManager.consumer is not None:
            consume(KafkaManager.consumer)


        

# Start Kafka consumer in a separate thread
thread = threading.Thread(target=consuming, daemon=True)
thread.start()

@app.route("/schedule", methods=["POST"])
def create_timeslot_assignment():

    data = request.get_json()
    if data is None:
        return jsonify({"code": 400, "message": "Invalid JSON format in the request.", "request": request.data.decode('utf-8')}), 400

    # expected input is 
    # {
        # "desired_timeslot": 1234
    # }
    desired_timeslot = data["desired_timeslot"]
    # passed time is seconds since epoch. convert to milliseconds for conversion to work properly
    desired_timeslot = datetime.fromtimestamp(int(desired_timeslot), timezone.utc)
    print(desired_timeslot)
    assignable_drivers = db.session.scalars(db.select(Schedule).filter(Schedule.timeslot == desired_timeslot, Schedule.assigned == False)).all()
    if assignable_drivers == []:
        return (
            jsonify(
                {
                    "code": 404,
                    "message": "No drivers are available for the desired timeslot.",
                    "desired_timeslot": desired_timeslot
                }
            ),
            404
        )
    
    random.shuffle(assignable_drivers)
    driver_found = False
    for driver in assignable_drivers:
        if redis_utils.lock_schedule(driver.id):
            driver_found = True
            assigned_driver = driver
            break
    
    
    if driver_found == False:
        print("redis lock working")
        return (
            jsonify(
                {
                    "code": 404,
                    "message": "No drivers are available for the desired timeslot. Redis lock is working as intended.",
                }
            ),
            404
        )
        

    # update status of assigned driver
    assigned_driver.assigned = True
    try:
        # commit the changes to the assigned driver to the database
        db.session.commit()
        redis_utils.unlock_schedule(assigned_driver.id)
    except Exception as e:
        print("Exception:{}".format(str(e)))
        return (
            jsonify(
                {
                    "code": 500,
                    "message": "An error occurred updating the schedule.",
                }
            ),
            500,
        )

    
    return jsonify({"code": 201, "data": assigned_driver.json()}), 201


@app.route("/available_slots", methods=["GET"])
def get_available_slots():
    """
    Returns the available timeslots within a given time range.
    Query parameters:
    - start: start timestamp (in seconds since epoch)
    - end: end timestamp (in seconds since epoch)
    """
    start_timestamp = request.args.get('start')
    end_timestamp = request.args.get('end')
    
    if not start_timestamp or not end_timestamp:
        return jsonify({"code": 400, "message": "Missing start or end timestamp"}), 400
    
    try:
        # Convert to datetime objects
        start_time = datetime.fromtimestamp(int(start_timestamp), timezone.utc)
        end_time = datetime.fromtimestamp(int(end_timestamp), timezone.utc)
        
        # Query for all unassigned timeslots in the range
        available_timeslots = db.session.query(Schedule.timeslot)\
            .filter(Schedule.timeslot >= start_time)\
            .filter(Schedule.timeslot <= end_time)\
            .filter(Schedule.assigned == False)\
            .distinct()\
            .all()
        
        # Extract the timestamp values and convert to Unix time
        available_slots = [int(ts[0].timestamp()) for ts in available_timeslots]
        
        return jsonify({"code": 200, "data": available_slots}), 200
    
    except Exception as e:
        print(f"Error retrieving available slots: {str(e)}")
        traceback.print_exc()
        return jsonify({"code": 500, "message": f"Error retrieving available slots: {str(e)}"}), 500


@app.route("/message", methods=["GET"])
def get_messages():
    """ Returns the last consumed messages from Kafka. """
    global messages
    print(messages)
    return jsonify({"messages": messages}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True, threaded=True)