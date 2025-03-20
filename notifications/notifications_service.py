from flask import Flask, request, jsonify
from firebase.firebase_db import save_notification, get_user_notifications, publish_notification
from firebase.firebase_config import firebase_admin
import os
import sys

# First, initialize Firebase
try:
    from firebase.firebase_config import firebase_admin
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

app = Flask(__name__)

@app.route('/notify', methods=['POST'])
def send_notification():
    """API endpoint to send a notification"""
    data = request.json
    
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
        
        # Publish to RabbitMQ
        publish_notification(user_id, fcm_token, title, body)
        
        return jsonify({
            "success": True,
            "message": "Notification queued for delivery",
            "notification_id": notification_id
        })
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/notifications/<user_id>', methods=['GET'])
def get_notifications_route(user_id):
    """API endpoint to get a user's notifications"""
    try:
        limit = request.args.get('limit', default=10, type=int)
        notifications = get_user_notifications(user_id, limit)
        return jsonify({"notifications": notifications})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "notifications"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)