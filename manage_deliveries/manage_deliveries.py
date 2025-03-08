from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv, dotenv_values
from datetime import datetime, timezone
from invokes import invoke_http

app = Flask(__name__)

CORS(app)

user_URL = "http://localhost:5000/user"


def processPlaceDeliveryRequest(delivery):
    #1 get the user info
    user_information = invoke_http(user_URL + "/user/" + str(delivery["user_id"]), method='GET')

@app.route("/place_delivery_request", methods=['POST'])
def place_delivery_request():
# Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            delivery = request.get_json()
            print("\nReceived a delivery request in JSON:", delivery)

            # do the actual work
            # 1. Send order info {cart items}
            result = processPlaceDeliveryRequest(delivery)
            return jsonify(result), result["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "place_order.py internal error: " + ex_str
            }), 500


    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400

    


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
