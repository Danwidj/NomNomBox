import json
import pika
import os
import sys
import time

# Add the current directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Import Firebase modules
try:
    from firebase import firebase_config
    from firebase_admin import messaging
    print("Firebase modules imported successfully")
except Exception as e:
    print(f"Error importing Firebase modules: {e}")
    sys.exit(1)

# RabbitMQ connection details
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", "5672"))
RABBITMQ_EXCHANGE = os.getenv("RABBITMQ_EXCHANGE", "notification_topic")
RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE", "notification_queue")
RABBITMQ_ROUTING_KEY = os.getenv("RABBITMQ_ROUTING_KEY", "notification.fcm")

print(f"RabbitMQ settings: {RABBITMQ_HOST}:{RABBITMQ_PORT}, Exchange: {RABBITMQ_EXCHANGE}, Queue: {RABBITMQ_QUEUE}")

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
    print(f"Received message: {body}")
    try:
        data = json.loads(body)
        user_id = data.get('user_id')
        fcm_token = data.get('fcm_token')
        title = data.get('title')
        body_text = data.get('body')
        
        print(f"Processing notification for user {user_id}")
        
        # Send FCM notification
        success = send_fcm_notification(fcm_token, title, body_text)
        
        if success:
            # Acknowledge message
            ch.basic_ack(delivery_tag=method.delivery_tag)
            print("Message acknowledged")
        else:
            # Negative acknowledgment - requeue the message
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
            print("Message negative acknowledged (requeued)")
            
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
    print("Starting consumer...")
    # Connect to RabbitMQ with retry logic
    connection = None
    while connection is None:
        try:
            print(f"Attempting to connect to RabbitMQ at {RABBITMQ_HOST}:{RABBITMQ_PORT}")
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=RABBITMQ_HOST,
                    port=RABBITMQ_PORT
                )
            )
            print("Connected to RabbitMQ")
        except pika.exceptions.AMQPConnectionError as e:
            print(f"Failed to connect to RabbitMQ: {e}")
            print("Retrying in 5 seconds...")
            time.sleep(5)
    
    channel = connection.channel()
    print("Channel created")
    
    # Ensure exchange exists
    channel.exchange_declare(
        exchange=RABBITMQ_EXCHANGE,
        exchange_type='topic',
        durable=True
    )
    print(f"Exchange '{RABBITMQ_EXCHANGE}' declared")
    
    # Ensure queue exists
    channel.queue_declare(
        queue=RABBITMQ_QUEUE,
        durable=True
    )
    print(f"Queue '{RABBITMQ_QUEUE}' declared")
    
    # Ensure queue is bound to exchange
    channel.queue_bind(
        exchange=RABBITMQ_EXCHANGE,
        queue=RABBITMQ_QUEUE,
        routing_key=RABBITMQ_ROUTING_KEY
    )
    print(f"Queue bound to exchange with routing key '{RABBITMQ_ROUTING_KEY}'")
    
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
        print("Consumer stopped by user")
    except Exception as e:
        print(f"Consumer stopped due to error: {e}")