import json
import pika
import os
import time
from firebase_admin import messaging
from firebase.firebase_config import firebase_admin  # This should initialize Firebase

# RabbitMQ connection details
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", "5672"))
RABBITMQ_EXCHANGE = os.getenv("RABBITMQ_EXCHANGE", "notification_topic")
RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE", "notification_queue")
RABBITMQ_ROUTING_KEY = os.getenv("RABBITMQ_ROUTING_KEY", "notification.fcm")

def send_fcm_notification(fcm_token, title, body):
    """Send notification via Firebase Cloud Messaging"""
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body
        ),
        token=fcm_token
    )
    
    try:
        response = messaging.send(message)
        print(f"Successfully sent notification: {response}")
        return True
    except Exception as e:
        print(f"Error sending FCM notification: {e}")
        return False

def process_message(ch, method, properties, body):
    """Process message from RabbitMQ"""
    try:
        data = json.loads(body)
        user_id = data.get('user_id')
        fcm_token = data.get('fcm_token')
        title = data.get('title')
        body = data.get('body')
        
        print(f"Processing notification for user {user_id}")
        
        # Send FCM notification
        success = send_fcm_notification(fcm_token, title, body)
        
        if success:
            # Acknowledge message
            ch.basic_ack(delivery_tag=method.delivery_tag)
        else:
            # Negative acknowledgment - requeue the message
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
            
    except json.JSONDecodeError:
        print(f"Invalid JSON in message: {body}")
        # Don't requeue if the message is invalid
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"Error processing message: {e}")
        # Requeue on other errors
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

def start_consumer():
    """Start the RabbitMQ consumer"""
    # Connect to RabbitMQ with retry logic
    connection = None
    while connection is None:
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=RABBITMQ_HOST,
                    port=RABBITMQ_PORT
                )
            )
        except pika.exceptions.AMQPConnectionError:
            print("Failed to connect to RabbitMQ. Retrying in 5 seconds...")
            time.sleep(5)
    
    channel = connection.channel()
    
    # Ensure queue exists
    channel.queue_declare(
        queue=RABBITMQ_QUEUE,
        durable=True
    )
    
    # Ensure queue is bound to exchange
    channel.queue_bind(
        exchange=RABBITMQ_EXCHANGE,
        queue=RABBITMQ_QUEUE,
        routing_key=RABBITMQ_ROUTING_KEY
    )
    
    # Set QoS - don't give more than one message to a worker at a time
    channel.basic_qos(prefetch_count=1)
    
    # Set up consumer
    channel.basic_consume(
        queue=RABBITMQ_QUEUE,
        on_message_callback=process_message
    )
    
    print(f"Starting consumer, listening for messages on {RABBITMQ_QUEUE}...")
    channel.start_consuming()

if __name__ == "__main__":
    try:
        start_consumer()
    except KeyboardInterrupt:
        print("Consumer stopped")