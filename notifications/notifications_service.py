from flask import Flask, request, jsonify
import os
import sys
import json
import pika

# Add the current directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# First, initialize Firebase
try:
    # Import the firebase_config module to ensure initialization happens
    from firebase import firebase_config
    print("Firebase initialization imported")
except Exception as e:
    print(f"Error importing Firebase config: {e}")
    sys.exit(1)

# Then import other Firebase-dependent modules
try:
    from firebase.firebase_db import save_notification, get_user_notifications, publish_notification
    print("Firebase DB functions imported successfully")
except Exception as e:
    print(f"Error importing Firebase DB functions: {e}")
    sys.exit(1)

# RabbitMQ connection details
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", "5672"))
RABBITMQ_EXCHANGE = os.getenv("RABBITMQ_EXCHANGE", "notification_topic")
RABBITMQ_ROUTING_KEY = os.getenv("RABBITMQ_ROUTING_KEY", "notification.fcm")

app = Flask(__name__)

@app.route('/notify', methods=['POST'])
def send_notification():
    """API endpoint to send a notification"""
    print("Received request to /notify endpoint")
    data = request.json
    print(f"Request data: {data}")
    
    # Validate request
    required_fields = ['user_id', 'fcm_token', 'title', 'body']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    user_id = data['user_id']
    fcm_token = data['fcm_token']
    title = data['title']
    body = data['body']
    
    try:
        # Save notification to Firestore
        notification_id = save_notification(user_id, title, body)
        print(f"Notification saved with ID: {notification_id}")
        
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
                "user_id": user_id,
                "fcm_token": fcm_token,
                "title": title,
                "body": body
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
            # Still return success since we saved to Firestore
        
        return jsonify({
            "success": True,
            "message": "Notification queued for delivery",
            "notification_id": notification_id
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
    print("Health check requested")
    return jsonify({"status": "healthy", "service": "notifications"})

@app.route('/')
def index():
    """Root endpoint for testing"""
    return jsonify({"message": "Notifications service is running"})

if __name__ == '__main__':
    print(f"Starting Flask app on port 8000")
    app.run(host='0.0.0.0', port=8000, debug=True)