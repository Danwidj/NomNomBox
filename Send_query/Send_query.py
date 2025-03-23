from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Service URLs
CUSTOMER_SERVICE_URL = "http://localhost:5002"  # Customer service
ORDER_SERVICE_URL = "http://localhost:5003"     # Order service
INVENTORY_SERVICE_URL = "http://localhost:5006"  # Inventory service
CHATBOT_SERVICE_URL = "http://localhost:5009"   # Chatbot service

@app.route("/api/recommendations/<customer_id>", methods=["POST"])
def get_meal_recommendations(customer_id):
    try:
        prompt = request.json.get("prompt")
        # Step 3: Fetch customer details (preferences)
        token = request.headers.get("Authorization")
        print(customer_id)
        if not customer_id:
            return jsonify({"error": "Customer ID is required", "response": customer_response.json()}), 400
        
        customer_response = requests.get(
            f"{CUSTOMER_SERVICE_URL}/customer/{customer_id}",
            headers={"Authorization": token}
        )
        if customer_response.status_code != 200:
            return jsonify({"error": "Failed to fetch customer details", "response": customer_response.json()}), 500
        
        customer_data = customer_response.json()
        
        # Step 5: Fetch past orders
        orders_response = requests.get(
            f"{ORDER_SERVICE_URL}/api/orders/customer/{customer_id}"
        )
        
        # Handle both 200 and 404 responses for orders
        if orders_response.status_code == 404:
            order_history = []  # Empty list if no orders found
        elif orders_response.status_code == 200:
            order_history = orders_response.json().get("data", [])
        else:
            return jsonify({"error": "Failed to fetch order history", "response": orders_response.json()}), 500
        
        # Step 7: Fetch available meal kits
        inventory_response = requests.get(
            f"{INVENTORY_SERVICE_URL}/inventory"
        )
        if inventory_response.status_code != 200:
            return jsonify({"error": "Failed to fetch available meal kits", "response": inventory_response.json()}), 500
        
        inventory = inventory_response.json()
        
        # Step 9: Send data to chatbot for recommendation
        chatbot_payload = {
            "prompt": prompt,
            "dietary_preferences": customer_data.get("dietary_preferences", {}),
            "order_history": order_history,
            "inventory": inventory.get("data", [])
        }
        
        chatbot_response = requests.post(
            f"{CHATBOT_SERVICE_URL}/generate-recommendation",
            json=chatbot_payload
        )
        
        if chatbot_response.status_code != 200:
            return jsonify({"error": "Failed to get recommendations", "response": chatbot_response.json()}), 500
        
        # Step 12: Return recommendations to UI
        return jsonify(chatbot_response.json()), 200

    except requests.RequestException as e:
        return jsonify({"error": f"Service communication error: {str(e)}", "response": chatbot_response.json()}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}", "response": chatbot_response.json()}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5100, debug=True) 