import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, request, jsonify
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Load Firebase credentials & prevent multiple initializations
if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

# Connect to Firestore
db = firestore.client()
customers_ref = db.collection("customers")

# Create a new customer (POST)
@app.route("/customer", methods=["POST"])
def create_customer():
    data = request.json
    new_customer_ref = customers_ref.document()  # Auto-generate ID
    new_customer_ref.set(data)

    # Include Firestore-generated ID in response
    return jsonify({
        "code": 201,
        "message": "Customer added",
        "data": {
            "id": new_customer_ref.id,
            **data
        }
    }), 201

# Get all customers (GET)
@app.route("/customer", methods=["GET"])
def get_all_customers():
    customers = [
        {"id": doc.id, **doc.to_dict()}  
        for doc in customers_ref.stream()
    ]
    if customers:
        return jsonify({"code": 200, "data": customers}), 200
    return jsonify({"code": 404, "message": "No customers found"}), 404

# Get a specific customer by ID (GET)
@app.route("/customer/<customer_id>", methods=["GET"])
def get_customer_by_id(customer_id):
    customer = customers_ref.document(customer_id).get()
    if customer.exists:
        return jsonify({"code": 200, "data": {"id": customer.id, **customer.to_dict()}}), 200
    return jsonify({"code": 404, "message": "Customer not found"}), 404

# Update a customer (PUT)
@app.route("/customer/<customer_id>", methods=["PUT"])
def update_customer(customer_id):
    customer = customers_ref.document(customer_id)
    if customer.get().exists:
        customer.update(request.json)
        return jsonify({"code": 200, "message": "Customer updated"}), 200
    return jsonify({"code": 404, "message": "Customer not found"}), 404

# Delete a customer (DELETE)
@app.route("/customer/<customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    customer = customers_ref.document(customer_id)
    if customer.get().exists:
        customer.delete()
        return jsonify({"code": 200, "message": "Customer deleted"}), 200
    return jsonify({"code": 404, "message": "Customer not found"}), 404

# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
