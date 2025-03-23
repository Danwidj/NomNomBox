import json
import pika
import os
import sys
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import requests  # Import the requests library
import string

load_dotenv()  # Load environment variables from .env file

# RabbitMQ connection details
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "127.0.0.1")  # or esd-rabbit once on docker
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", "5672"))
RABBITMQ_EXCHANGE = os.getenv("RABBITMQ_EXCHANGE", "notification_topic")
NOTIFICATIONS_QUEUE = os.getenv("NOTIFICATIONS_QUEUE", "notification_queue") # get Notifications queue name

# Email configuration
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SENDER_EMAIL = os.getenv("SENDER_EMAIL", SMTP_USERNAME)

# Order service URL
ORDER_SERVICE_URL = os.getenv("ORDER_SERVICE_URL", "http://localhost:5003/api/orders")
CUSTOMER_SERVICE_URL = os.getenv("CUSTOMER_SERVICE_URL", "http://localhost:5002/customer") #added line
DELIVERY_PICKEDUP_TEMPLATE = os.getenv("DELIVERY_PICKEDUP_TEMPLATE","Dear Customer,\n\nYour delivery {delivery_id} status has been updated to {status} \nThank you for your order!\n")


print(
    f"RabbitMQ settings: {RABBITMQ_HOST}:{RABBITMQ_PORT}, Exchange: {RABBITMQ_EXCHANGE}"
)


def send_email(recipient_email, subject, message_body):
    """Send an email to the specified recipient"""
    if not all([SMTP_SERVER, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD]):
        print("Email configuration incomplete. Skipping email send.")
        return False

    try:
        # Create message
        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = recipient_email
        msg["Subject"] = subject

        # Attach message body
        msg.attach(MIMEText(message_body, "plain"))

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
        routing_key = method.routing_key

        if routing_key == "order.payment_success": # changed routing key
            # Process 'order.payment_success' message
            order_id = data.get("orderId")
            customer_id = data.get("customer_id") # Added line

            # Get user email
            customer_url = f"{CUSTOMER_SERVICE_URL}/{customer_id}" # Customer service URL
            customer_response = requests.get(customer_url)
            customer_response.raise_for_status() # If error occurs, raise http error
            customer_data = customer_response.json().get("data", {})
            customer_email = customer_data.get("email") # Gets the user email
            # Placeholder - you need to retrieve the email from the user ID.

            subject = f"Payment Successful - Order #{order_id}"
            body_text = f"Your payment for order #{order_id} with session ID  was successful!"

            if not customer_email:
                print(f"No email address found for delivery_id. Skipping.")
                ch.basic_ack(delivery_tag=method.delivery_tag)
                return

            email_success = send_email(customer_email, subject, body_text)

        elif routing_key in ( #Change condition of key routing here
            "delivery.pickedup",
            "delivery.delivered",
            "delivery.received",
            "delivery.assigned",
        ):
            # Process delivery status updates
            delivery_id = data.get("delivery_id")
            status = data.get("status")
            customer_id = data.get("customer_id")  # Added Line for access


            # Get user email
            customer_url = f"{CUSTOMER_SERVICE_URL}/{customer_id}" # Customer service URL
            customer_response = requests.get(customer_url)
            customer_response.raise_for_status() # If error occurs, raise http error
            customer_data = customer_response.json().get("data", {})
            customer_email = customer_data.get("email") # Gets the user email
            # Placeholder - you need to retrieve the email from the user ID.

            subject = f"Delivery Status Update - Delivery #{delivery_id}"
            # body_text = f"Your delivery #{delivery_id} status has been updated to {status}."
            template = string.Template(DELIVERY_PICKEDUP_TEMPLATE) # set template
            body_text = template.substitute(delivery_id=delivery_id,status=status)

            if not customer_email:
                print(f"No email address found for delivery_id. Skipping.")
                ch.basic_ack(delivery_tag=method.delivery_tag)
                return

            email_success = send_email(customer_email, subject, body_text)

        else:
            print(f"Unknown routing key: {routing_key}. Skipping.")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return

        if email_success:
            ch.basic_ack(delivery_tag=method.delivery_tag)
            print("Message acknowledged")
        else:
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
            print("Message negative acknowledged (requeued)")

    except json.JSONDecodeError:
        print(f"Invalid JSON in message: {body}")
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"Error processing message: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)


def start_consumer():
    """Start the RabbitMQ consumer"""
    print("Starting consumer...")
    # Connect to RabbitMQ with retry logic
    connection = None
    while connection is None:
        try:
            print(
                f"Attempting to connect to RabbitMQ at {RABBITMQ_HOST}:{RABBITMQ_PORT}"
            )
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT)
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
        exchange=RABBITMQ_EXCHANGE, exchange_type="topic", durable=True
    )
    print(f"Exchange '{RABBITMQ_EXCHANGE}' declared")

    queue_name = NOTIFICATIONS_QUEUE # changed to static queues
    print(f"Queue '{queue_name}' declared")


    channel.basic_qos(prefetch_count=1)

    # Set up consumer
    channel.basic_consume(queue=queue_name, on_message_callback=process_message) # process_message function

    print(f"Starting consumer, listening for messages on {queue_name}...")
    channel.start_consuming()


if __name__ == "__main__":
    try:
        start_consumer()

    except KeyboardInterrupt:
        print("Consumer stopped by user")
    except Exception as e:
        print(f"Consumer stopped due to error: {e}")