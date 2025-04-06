from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": "*",  # Allow all origins
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "expose_headers": ["Content-Type", "Authorization"]
    }
})

# Service URLs
CUSTOMER_SERVICE_URL = "http://customer:5002"  # Customer service
ORDER_SERVICE_URL = "http://order:5003"     # Order service
INVENTORY_SERVICE_URL = "http://inventory:5006"  # Inventory service
CHATBOT_SERVICE_URL = "http://gemini:5009"   # Chatbot service
CHAT_HISTORY_URL = "http://chathistory:5012"      # Chat history service

@app.route("/api/recommendations/<customer_id>", methods=["POST"])
def get_meal_recommendations(customer_id):
    try:
        prompt = request.json.get("prompt")
        # Step 3: Fetch customer details (preferences)
        token = request.headers.get("Authorization")
        print(customer_id)
        if not customer_id:
            return jsonify({"error": "Customer ID is required"}), 400
        
        # Fetch chat history first
        chat_history_response = requests.get(
            f"{CHAT_HISTORY_URL}/chat/{customer_id}",
            headers={"Authorization": token}
        )
        chat_history = []
        if chat_history_response.status_code == 200:
            chat_history = chat_history_response.json().get('messages', [])
        
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
            "chat_history": chat_history,  # Add chat history to context
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
        
        # Get the chatbot response data
        chatbot_data = chatbot_response.json()
        
        # Create a proper timezone-aware datetime object for SGT (UTC+8)
        sgt_tz = timezone(timedelta(hours=8))
        current_time = datetime.now(sgt_tz).strftime("%Y-%m-%dT%H:%M:%S+08:00")
        
        # Save both prompt and response in a single document
        chat_response = requests.post(
            f"{CHAT_HISTORY_URL}/chat/{customer_id}",
            headers={"Authorization": token},
            json={
                "created_at": current_time,
                "prompt": prompt,
                "recommended_meal_kits": chatbot_data.get("recommended meal-kit", []),
                "response": chatbot_data.get("response", ""),
                "role": "model"
            }
        )
        
        if chat_response.status_code != 200:
            print(f"Failed to save chat history: {chat_response.text}")
        
        # Step 12: Return recommendations to UI
        return jsonify(chatbot_data), 200

    except requests.RequestException as e:
        return jsonify({"error": f"Service communication error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5100, debug=True) 