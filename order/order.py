from flask import Flask, jsonify, request
from flask_cors import CORS
from firebase_config import db
import requests
import os
import stripe
import firebase_admin
from firebase_admin import firestore
app = Flask(__name__)
CORS(app)  # Allow CORS for frontend access

#  Fetch Inventory Data from the Inventory Microservice API
@app.route("/api/orders/inventory", methods=["GET"])
def get_inventory():
    try:
        inventory_api_url = "http://localhost:5006/inventory"  # Inventory Microservice
        response = requests.get(inventory_api_url)

        if response.status_code == 200:
            return jsonify(response.json()), 200
        else:
            return jsonify({"code": response.status_code, "message": "Error fetching inventory"}), response.status_code
    except Exception as e:
        return jsonify({"code": 500, "message": f"Internal Server Error: {str(e)}"}), 500

#  Place an order
@app.route("/api/orders/place", methods=["POST"])
def place_order():
    try:
        data = request.json
        required_fields = ["customerId", "items", "totalPrice"]

        if not all(field in data for field in required_fields):
            return jsonify({"code": 400, "message": "Missing required fields"}), 400

        # Save order in Firestore
        order_ref = db.collection("Orders").document()
        order_data = {
            "orderId": order_ref.id,
            "customerId": data["customerId"],
            "items": data["items"],
            "totalPrice": data["totalPrice"],
            "status": "pending",
            "paymentIntentId": None,
            "createdAt": firestore.SERVER_TIMESTAMP,
            "updatedAt": firestore.SERVER_TIMESTAMP
        }
        order_ref.set(order_data)

      

        return jsonify({
            "code": 201,
            "message": "Order placed successfully",
            "orderId": order_ref.id
            
        }), 201

    except Exception as e:
        return jsonify({"code": 500, "message": f"Error placing order: {str(e)}"}), 500


# Update Order with Payment Intent ID and Mark as Paid
@app.route("/api/orders/update-payment", methods=["POST"])
def update_payment():
    try:
        data = request.json
        required_fields = ["orderId", "paymentIntentId"]

        if not all(field in data for field in required_fields):
            return jsonify({"code": 400, "message": "Missing required fields"}), 400

        order_ref = db.collection("Orders").document(data["orderId"])
        order_ref.update({
            "paymentIntentId": data["paymentIntentId"],
            "status": "paid",  #  Mark order as paid
            "updatedAt": firestore.SERVER_TIMESTAMP
        })

        return jsonify({"code": 200, "message": "Order updated as paid"}), 200

    except Exception as e:
        return jsonify({"code": 500, "message": f"Error updating order: {str(e)}"}), 500

# Get Order by Order ID
@app.route("/api/orders/<string:order_id>", methods=["GET"])
def get_order(order_id):
    try:
        order_ref = db.collection("Orders").document(order_id)
        order_doc = order_ref.get()

        if not order_doc.exists:
            return jsonify({"code": 404, "message": "Order not found"}), 404

        order_data = order_doc.to_dict()
        return jsonify({"code": 200, "data": order_data}), 200

    except Exception as e:
        return jsonify({"code": 500, "message": f"Error fetching order: {str(e)}"}), 500


# Get All Orders for a Customer
@app.route("/api/orders/customer/<string:customer_id>", methods=["GET"])
def get_orders_by_customer(customer_id):
    try:
        orders_ref = db.collection("Orders").where("customerId", "==", customer_id).stream()
        orders = [order.to_dict() for order in orders_ref]

        if not orders:
            return jsonify({"code": 404, "message": "No orders found for this customer"}), 404

        return jsonify({"code": 200, "data": orders}), 200

    except Exception as e:
        return jsonify({"code": 500, "message": f"Error fetching orders: {str(e)}"}), 500
    

    
@app.route("/api/orders/{orderId}", methods=["PATCH"])
def place_orderr():
    try:
        data = request.json
        required_fields = ["orderId"]

        if not all(field in data for field in required_fields):
            return jsonify({"code": 400, "message": "Missing required fields"}), 400

        order_ref = db.collection("Orders").document(data["orderId"])

        fields_to_update = {}

        for key, value in data.items():
            if key != "orderId":
                fields_to_update[key] = value
        if fields_to_update:
            fields_to_update["updatedAt"] = firestore.SERVER_TIMESTAMP
            order_ref.update(fields_to_update)      

      

        return jsonify({
            "code": 201,
            "message": "Order placed successfully",
            "orderId": order_ref.id
            
        }), 201

    except Exception as e:
        return jsonify({"code": 500, "message": f"Error placing order: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(port=5003, debug=True)
