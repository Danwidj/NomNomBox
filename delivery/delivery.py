from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv, dotenv_values
from datetime import datetime, timezone

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




class Delivery(db.Model):
    __tablename__ = "delivery"


    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.TIMESTAMP(timezone=True), nullable=False)
    end_time = db.Column(db.TIMESTAMP(timezone=True), nullable=False)
    location = db.Column(db.Text, nullable=False)
    driver_id = db.Column(db.Integer, nullable=False)



    def __init__(self, order_id, start_time, end_time, location, driver_id):
        self.order_id = order_id
        self.start_time = start_time
        self.end_time = end_time
        self.location = location
        self.driver_id = driver_id


    def json(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "driver_id": self.driver_id,
            "location": self.location,
        }

def get_delivery_by_time(start_time, end_time):
    start_time = datetime.fromtimestamp(int(start_time), timezone.utc)
    end_time = datetime.fromtimestamp(int(end_time), timezone.utc)
    print(start_time, end_time)
    delivery_list = db.session.scalars(db.select(Delivery).filter(Delivery.start_time >= start_time, Delivery.end_time <= end_time)).all()

    if len(delivery_list):
        return jsonify(
            {
                "code": 200,
                "data": {"deliveries": [delivery.json() for delivery in delivery_list]},
            }
        )
    return jsonify({"code": 404, "message": "There are no deliveries for this time period."}), 404

def get_delivery_by_driver(driver_id):
    delivery_list = db.session.scalars(db.select(Delivery).filter(Delivery.driver_id == driver_id)).all()

    if len(delivery_list):
        return jsonify(
            {
                "code": 200,
                "data": {"deliveries": [delivery.json() for delivery in delivery_list]},
            }
        )
    return jsonify({"code": 404, "message": "There are no deliveries for this driver."}), 404

def get_delivery_by_order(order_id):
    delivery_list = db.session.scalars(db.select(Delivery).filter(Delivery.order_id == order_id)).all()
    if len(delivery_list):
        return jsonify(
            {
                "code": 200, 
                "data": {"deliveries": [delivery.json() for delivery in delivery_list]}
        }
    )
    return jsonify({"code": 404, "message": "Delivery not found."}), 404

@app.route("/delivery")
def get_deliveries():
    if request.args.get("start_time") and request.args.get("end_time"):
        start_time = request.args.get("start_time")
        end_time = request.args.get("end_time")
        print(start_time, end_time)
        return get_delivery_by_time(start_time, end_time)

    elif request.args.get("driver_id"):
        driver_id = request.args.get("driver_id")
        return get_delivery_by_driver(driver_id)
    
    elif request.args.get("order_id"):
        order_id = request.args.get("order_id")
        return get_delivery_by_order(order_id)
    
    else:
        delivery_list = db.session.scalars(db.select(Delivery)).all()

        if len(delivery_list):
            return jsonify(
                {
                    "code": 200,
                    "data": {"deliveries": [delivery.json() for delivery in delivery_list]},
                }
            )
        return jsonify({"code": 404, "message": "There are no deliveries."}), 404


@app.route("/delivery/<int:id>")
def get_delivery(id):
    delivery = db.session.scalar(db.select(Delivery).filter_by(id=id))

    if delivery:
        return jsonify({"code": 200, "data": delivery.json()})
    return jsonify({"code": 404, "message": "Delivery not found."}), 404


@app.route("/delivery", methods=["POST"])
def create_delivery():

    data = request.get_json()
    delivery = Delivery(**data)

    try:
        db.session.add(delivery)
        db.session.commit()
    except Exception as e:
        print("Exception:{}".format(str(e)))
        return (
            jsonify(
                {
                    "code": 500,
                    "message": "An error occurred creating the delivery.",
                }
            ),
            500,
        )

    return jsonify({"code": 201, "data": delivery.json()}), 201

@app.route("/delivery/<int:id>", methods=["PUT"])
def update_delivery(id):
    delivery = db.session.scalar(db.select(Delivery).filter_by(id=id))

    if not delivery:
        return jsonify({"code": 404, "message": "Delivery not found."}), 404

    data = request.get_json()

    for key, value in data.items():
        setattr(delivery, key, value)

    try:
        db.session.commit()
    except Exception as e:
        print("Exception:{}".format(str(e)))
        return (
            jsonify(
                {
                    "code": 500,
                    "message": "An error occurred updating the delivery.",
                }
            ),
            500,
        )

    return jsonify({"code": 200, "data": delivery.json()}), 200





if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
