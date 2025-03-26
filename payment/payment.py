from flask import Flask, request, jsonify
import stripe
import os
import requests  # Import requests to communicate with the order service
from firebase_admin import firestore

from flask_cors import CORS

app = Flask(__name__)
CORS(app)  #  allows frontend acces

# Set Stripe API Key
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# Order Service API URL
ORDER_SERVICE_URL = "http://localhost:5003/api/orders/update-payment"

#  Create a Stripe Checkout Session (Instead of PaymentIntent)
@app.route("/api/payment/create", methods=["POST"])
def create_payment():
    try:
        data = request.json
        required_fields = ["orderId", "amount", "items"]

        if not all(field in data for field in required_fields):
            return jsonify({"code": 400, "message": "Missing required fields"}), 400

        #  Convert items to Stripe Checkout format
        line_items = [
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": item["name"],
                    },
                    "unit_amount": int(item["price"] * 100),  # Convert dollars to cents
                },
                "quantity": item["quantity"],
            }
            for item in data["items"]
        ]

        # Create Stripe Checkout Session
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=line_items,
            mode="payment",
            success_url="http://localhost:5173/success?session_id={CHECKOUT_SESSION_ID}",  # Redirect URL after payment
            cancel_url="http://localhost:5173/Cart",  # Redirect URL if payment is cancelled
            metadata={"orderId": data["orderId"]}
        )

        return jsonify({
            "code": 201,
            "message": "Checkout session created",
            "sessionId": session.id  #  Return sessionId
        }), 201

    except Exception as e:
        return jsonify({"code": 500, "message": f"Error creating payment session: {str(e)}"}), 500


    
@app.route("/api/payment/public-key", methods=["GET"])
def get_stripe_public_key():
    public_key = os.getenv("STRIPE_PUBLIC_KEY")  # Fetch the key
    if not public_key:
        return jsonify({"error": "Stripe public key is missing"}), 500
    return jsonify({"publicKey": public_key})

# Stripe Webhook: Update Firestore When Payment Is Successful
# @app.route("/webhook", methods=["POST"])
# def stripe_webhook():
#     payload = request.get_data(as_text=True)
#     sig_header = request.headers.get("Stripe-Signature")

#     try:
#         event = stripe.Webhook.construct_event(payload, sig_header, os.getenv("STRIPE_WEBHOOK_SECRET"))

#         if event["type"] == "payment_intent.succeeded":
#             payment_intent = event["data"]["object"]
#             order_id = payment_intent["metadata"]["orderId"]

#             #  Update Firestore order status to "paid"
#             order_ref = db.collection("Orders").document(order_id)
#             order_ref.update({
#                 "status": "paid",
#                 "updatedAt": firestore.SERVER_TIMESTAMP
#             })
#             print(f" Order {order_id} marked as paid!")

#         return jsonify(success=True), 200

#     except stripe.error.SignatureVerificationError as e:
#         return jsonify({"error": f"Webhook signature error: {str(e)}"}), 400

#     except Exception as e:
#         return jsonify({"error": f"Webhook handling error: {str(e)}"}), 500
@app.route("/api/payment/status", methods=["GET"])
def get_payment_status():
    session_id = request.args.get("session_id")

    if not session_id:
        return jsonify({"error": "Missing session_id"}), 400

    try:
        # ✅ Fetch session details from Stripe
        session = stripe.checkout.Session.retrieve(session_id)

        if session.payment_status != "paid":
            return jsonify({"status": session.payment_status, "message": "Payment not completed"}), 400

        return jsonify({
            "status": "complete",
            "orderId": session.metadata["orderId"]
        }), 200

    except Exception as e:
        return jsonify({"error": f"Error fetching payment status: {str(e)}"}), 500

# Run Payment Service on Port 5004
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004, debug=True)
