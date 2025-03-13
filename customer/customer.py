import os
import firebase_admin
from firebase_admin import credentials, firestore, auth
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS

# Load environment variables from .env
load_dotenv()

# Get Firebase credentials path from .env
firebase_credentials_path = os.getenv("FIREBASE_CREDENTIALS")

if not firebase_credentials_path:
    raise ValueError("Missing FIREBASE_CREDENTIALS in .env file")

# Initialize Firebase only if not already initialized
if not firebase_admin._apps:
    try:
        cred = credentials.Certificate(firebase_credentials_path)
        firebase_admin.initialize_app(cred)
    except Exception as e:
        raise RuntimeError(f"Failed to initialize Firebase: {e}")

# Initialize Flask app & Firestore
app = Flask(__name__)
CORS(app)
db = firestore.client()
customers_ref = db.collection("customers")


#Middleware: Verify Firebase ID Token
def verify_token():
    """Verifies Firebase ID token from Authorization header."""
    token = request.headers.get("Authorization")
    if not token or not token.startswith("Bearer "):
        return None, jsonify({"code": 401, "message": "No token provided"}), 401

    try:
        id_token = token.split("Bearer ")[1]  # Extract token
        decoded_token = auth.verify_id_token(id_token)  # Verify with Firebase
        return decoded_token, None
    except Exception as e:
        return None, jsonify({"code": 401, "message": "Invalid token", "error": str(e)}), 401


#Register a new user (Sign Up)
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    required_fields = ["email", "password", "name"]

    # Ensure all required fields are provided
    for field in required_fields:
        if field not in data:
            return jsonify({"code": 400, "message": f"Missing field: {field}"}), 400

    try:
        # Create user in Firebase Authentication
        user = auth.create_user(
            email=data["email"],
            password=data["password"],
            display_name=data.get("name", "")
        )

        # Store user details in Firestore
        customers_ref.document(user.uid).set({
            "email": data["email"],
            "name": data["name"],
            "address": data.get("address", ""),
            "phone": data.get("phone", ""),
            "dietary_preferences": data.get("dietary_preferences", ""),
        })

        return jsonify({"code": 201, "message": "User registered", "uid": user.uid}), 201
    except Exception as e:
        return jsonify({"code": 400, "message": str(e)}), 400

#Verify Firebase ID Token (Middleware)
def verify_token():
    """Verifies Firebase ID token from Authorization header."""
    token = request.headers.get("Authorization")
    if not token or not token.startswith("Bearer "):
        return None, jsonify({"code": 401, "message": "No token provided"}), 401

    try:
        id_token = token.split("Bearer ")[1]  # Extract token
        decoded_token = auth.verify_id_token(id_token)  # Verify with Firebase
        return decoded_token, None
    except Exception as e:
        return None, jsonify({"code": 401, "message": "Invalid token", "error": str(e)}), 401

#Authenticate a user (Login)
@app.route("/login", methods=["POST"])
def login():
    return jsonify({"message": "Firebase handles login client-side"}), 200


#Get customer details (Requires authentication)
@app.route("/customer/<customer_id>", methods=["GET"])
def get_customer_by_id(customer_id):
    decoded_token, error = verify_token()
    if error:
        return error  # Return authentication error if token is invalid

    customer = customers_ref.document(customer_id).get()
    if customer.exists:
        return jsonify({"code": 200, "data": {"id": customer.id, **customer.to_dict()}}), 200
    return jsonify({"code": 404, "message": "Customer not found"}), 404


#Get all customers
@app.route("/customer", methods=["GET"])
def get_all_customers():
    customers = [{"id": doc.id, **doc.to_dict()} for doc in customers_ref.stream()]
    if customers:
        return jsonify({"code": 200, "data": customers}), 200
    return jsonify({"code": 404, "message": "No customers found"}), 404


#Update customer details (Requires authentication)
@app.route("/customer/<customer_id>", methods=["PUT"])
def update_customer(customer_id):
    decoded_token, error = verify_token()
    if error:
        return error  # Return authentication error if token is invalid

    customer = customers_ref.document(customer_id)
    if customer.get().exists:
        customer.update(request.json)
        return jsonify({"code": 200, "message": "Customer updated"}), 200
    return jsonify({"code": 404, "message": "Customer not found"}), 404


#Delete customer (Requires authentication)
@app.route("/customer/<customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    decoded_token, error = verify_token()
    if error:
        return error  # Return authentication error if token is invalid

    customer = customers_ref.document(customer_id)
    if customer.get().exists:
        customer.delete()
        return jsonify({"code": 200, "message": "Customer deleted"}), 200
    return jsonify({"code": 404, "message": "Customer not found"}), 404


#Run Flask App
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
