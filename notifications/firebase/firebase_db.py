import json
import pika
from firebase_admin import firestore

# Initialize Firestore
db = firestore.client()

# RabbitMQ Connection
amqp_host = "localhost"
amqp_port = 5672
exchange_name = "notification_topic"

def publish_notification(user_id, fcm_token, title, body):
    """Publish notification event to RabbitMQ"""
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=amqp_host, port=amqp_port))
        channel = connection.channel()
        
        # Ensure exchange exists
        channel.exchange_declare(
            exchange=exchange_name, 
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
            exchange=exchange_name,
            routing_key="notification.fcm",
            body=json.dumps(message),
            properties=pika.BasicProperties(delivery_mode=2)
        )

        connection.close()
        return "Message published to RabbitMQ"
    except pika.exceptions.AMQPConnectionError as e:
        print(f"RabbitMQ connection error: {e}")
        raise
    except Exception as e:
        print(f"Error publishing notification: {e}")
        raise

def save_notification(user_id, title, body):
    """Save notification data to Firestore"""
    notification_ref = db.collection("notifications").document()
    notification_ref.set({
        "user_id": user_id,
        "title": title,
        "body": body,
        "read": False,
        "created_at": firestore.SERVER_TIMESTAMP
    })
    return notification_ref.id

def get_user_notifications(user_id, limit=10):
    """Get notifications for a user"""
    notifications = db.collection("notifications") \
                      .where("user_id", "==", user_id) \
                      .limit(limit) \
                      .stream()
    
    return [{"id": doc.id, **doc.to_dict()} for doc in notifications]