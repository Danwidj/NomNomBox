from flask import Flask, request, jsonify
import os
import json
import pika
from firebase import firebase_config
from firebase.firebase_db import save_notification, get_user_notifications

# RabbitMQ connection details
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "127.0.0.1")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", "5672"))
RABBITMQ_EXCHANGE = os.getenv("RABBITMQ_EXCHANGE", "notification_topic")
RABBITMQ_ROUTING_KEY = os.getenv("RABBITMQ_ROUTING_KEY", "order.payment_success")

app = Flask(__name__)

@app.route('/notify', methods=['POST'])
def send_notification():
    """API endpoint to send a payment success notification for troubleshooting"""
    print("Received request to /notify endpoint")
    data = request.json
    print(f"Request data: {data}")

    # Validate request - orderId, session_id, customer_id, customer_email are required
    required_fields = ['orderId', 'session_id', 'customer_id', 'customer_email'] #Refactoring

    if not all(field in data for field in required_fields):
        return jsonify({"error": f"Missing required field: {field}"}), 400

    order_id = data['orderId']
    session_id = data['session_id']
    customer_id = data['customer_id']
    customer_email = data['customer_email']

    try:
        # No need to save to Firestore for this troubleshooting endpoint
        # Publish to RabbitMQ
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT)
            )
            channel = connection.channel()

            # Ensure exchange exists
            channel.exchange_declare(
                exchange=RABBITMQ_EXCHANGE,
                exchange_type='topic',
                durable=True
            )

            message = {
                "orderId": order_id,
                "session_id": session_id,
                "customer_id": customer_id,
                "customer_email": customer_email
            }

            channel.basic_publish(
                exchange=RABBITMQ_EXCHANGE,
                routing_key=RABBITMQ_ROUTING_KEY,
                body=json.dumps(message),
                properties=pika.BasicProperties(delivery_mode=2)  # Make message persistent
            )

            connection.close()
            print("Message published to RabbitMQ")

        except Exception as e:
            print(f"Error publishing to RabbitMQ: {e}")
            return jsonify({"success": False, "message": f"Error publishing to RabbitMQ: {e}"}), 500

        return jsonify({
            "success": True,
            "message": "Payment success notification queued for delivery",
            "orderId": order_id,
            "customer_email": customer_email
        })

    except Exception as e:
        print(f"Error in send_notification: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/notifications/<user_id>', methods=['GET'])
def get_notifications_route(user_id):
    """API endpoint to get a user's notifications"""
    print(f"Received request to get notifications for user: {user_id}")
    try:
        limit = request.args.get('limit', default=10, type=int)
        notifications = get_user_notifications(user_id, limit)
        return jsonify({"notifications": notifications})
    except Exception as e:
        print(f"Error in get_notifications_route: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "notifications"})

@app.route('/')
def index():
    """Root endpoint for testing"""
    return jsonify({"message": "Notifications service is running"})

if __name__ == '__main__':
    print(f"Starting Flask app on port 8000")
    app.run(host='0.0.0.0', port=9000, debug=True)