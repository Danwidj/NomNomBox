import json
import pika
import os
import sys
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# RabbitMQ connection details
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "127.0.0.1") # or esd-rabbit once on docker
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", "5672"))
RABBITMQ_EXCHANGE = os.getenv("RABBITMQ_EXCHANGE", "notification_topic")
RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE", "notification_queue")
RABBITMQ_ROUTING_KEY = os.getenv("RABBITMQ_ROUTING_KEY", "notification.email")

# Email configuration
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SENDER_EMAIL = os.getenv("SENDER_EMAIL", SMTP_USERNAME)

print(f"RabbitMQ settings: {RABBITMQ_HOST}:{RABBITMQ_PORT}, Exchange: {RABBITMQ_EXCHANGE}, Queue: {RABBITMQ_QUEUE}")

def send_email(recipient_email, subject, message_body):
    """Send an email to the specified recipient"""
    if not all([SMTP_SERVER, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD]):
        print("Email configuration incomplete. Skipping email send.")
        return False
    
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = recipient_email
        msg['Subject'] = subject
        
        # Attach message body
        msg.attach(MIMEText(message_body, 'plain'))
        
        # Connect to SMTP server
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Secure the connection
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        
        # Send email
        server.send_message(msg)
        server.quit()
        
        print(f"Email sent successfully to {recipient_email}")
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def process_message(ch, method, properties, body):
    """Process message from RabbitMQ"""
    print(f"Received message: {body}")
    try:
        data = json.loads(body)
        user_id = data.get('user_id')
        email = data.get('email')
        title = data.get('title', 'Notification')
        body_text = data.get('body', '')
        
        print(f"Processing email notification for user {user_id}")
        
        if not email:
            print("No email address provided in message. Skipping.")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return
        
        # Send email
        email_success = send_email(email, title, body_text)
        
        if email_success:
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