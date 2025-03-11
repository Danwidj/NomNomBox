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

app = Flask(__name__)

CORS(app)
load_dotenv(".env")
print(os.getenv("DATABASE_HOST"))

app.config["SQLALCHEMY_DATABASE_URI"] = (
     os.getenv("DATABASE_HOST")
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

KAFKA_BROKER_URL = "localhost:9092"
KAFKA_TOPIC = "driver-schedule-updates"

messages = []




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
            "timeslot": self.timeslote,
            "assigned": self.assigned
        }

def consume(consumer):
    try:
        for msg in consumer:
            decoded_message = msg.value.decode('utf-8')
            print(f"Received: {decoded_message}")  # Log message
            messages.append(json.loads(decoded_message))  # Store message in memory
            

        print(f"Messages: {messages}")
            
    except Exception as e:
        print(f"Exception: {str(e)}")

def start_kafka_consumer():
    time.sleep(10)  # Wait for Kafka to start
    consumer = KafkaConsumer(
            KAFKA_TOPIC,
            bootstrap_servers=KAFKA_BROKER_URL,
            group_id="my-group",
            auto_offset_reset="earliest",
            heartbeat_interval_ms=1000,
    )
    global messages

    consume(consumer)


# Start Kafka consumer in a separate thread
thread = threading.Thread(target=start_kafka_consumer, daemon=True)
thread.start()

@app.route("/schedule", methods=["POST"])
def create_timeslot_assignment():

    data = request.get_json()
    # it gets 
    # {
        # "desired_timeslot": 1234
    # }
    desired_timeslot = data["desired_timeslot"]
    desired_timeslot = datetime.fromtimestamp(int(desired_timeslot), timezone.utc)
    assignable_drivers = db.session.scalars(db.select(Schedule).filter(Schedule.timeslot == desired_timeslot)).all()
    # pick driver randomly
    assigned_driver = random.choice(assignable_drivers)
    # update status of assigned driver
    assigned_driver.assigned = True
    try:
        # commit the changes to the assigned driver to the database
        db.session.commit()
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


@app.route("/message", methods=["GET"])
def get_messages():
    """ Returns the last 10 consumed messages from Kafka. """
    global messages
    print(messages)
    return jsonify({"messages": messages}), 200









if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
