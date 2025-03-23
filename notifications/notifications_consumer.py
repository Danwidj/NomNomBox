import json
import pika
import os
import sys
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests  # Import the requests library
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

# RabbitMQ connection details
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "127.0.0.1")  # or esd-rabbit once on docker
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", "5672"))
RABBITMQ_EXCHANGE = os.getenv("RABBITMQ_EXCHANGE", "notification_topic")
# Removed RABBITMQ_QUEUE and RABBITMQ_ROUTING_KEY
# Email configuration
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SENDER_EMAIL = os.getenv("SENDER_EMAIL", SMTP_USERNAME)

# Order & Customer service URLs
ORDER_SERVICE_URL = os.getenv("ORDER_SERVICE_URL", "http://localhost:5003/api/orders")
CUSTOMER_SERVICE_URL = os.getenv("CUSTOMER_SERVICE_URL", "http://localhost:5002/customer") #added line

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

        if routing_key == "delivery.assigned":
            # Process 'delivery.assigned' message
            email = data.get("email")
            delivery_time = data.get("delivery_time")
            order_id = data.get("order_id")
            name = data.get("name")
            status = data.get("status")

            if not email:
                print("No email address provided in message. Skipping.")
                ch.basic_ack(delivery_tag=method.delivery_tag)
                return

            subject = f"Delivery Assigned - Order #{order_id}"
            body_text = (
                f"Dear {name},\n\n"
                f"Your order #{order_id} has been assigned to a driver and is scheduled"
                f" for delivery around {delivery_time}.\n\n"
                f"Thank you for your order!\n"
            )
            email_success = send_email(email, subject, body_text)

        elif routing_key in (
            "delivery.pickedup",
            "delivery.delivered",
            "delivery.received",
        ):
            # Process delivery status updates
            delivery_id = data.get("delivery_id")
            status = data.get("status")

            subject = f"Delivery Status Update - Delivery #{delivery_id}"
            body_text = f"Your delivery #{delivery_id} status has been updated to {status}."
            # You would need to fetch the email from a database using delivery_id here
            # Replace with actual email retrieval logic

            # Placeholder to retrieve email - you need to replace this with your actual logic
            email = "esdg06t02@gmail.com" # Default email for debugging
            if not email:
                print("No email address found for delivery_id. Skipping.")
                ch.basic_ack(delivery_tag=method.delivery_tag)
                return

            email_success = send_email(email, subject, body_text)

        elif routing_key == "order.payment_success":  # Added logic to handle order.payment_success
            # Process 'order.payment_success' message
            order_id = data.get("orderId")
            customer_id = data.get("customer_id") # Added line
            # Fetch order details
            try:
                order_url = f"{ORDER_SERVICE_URL}/{order_id}"
                order_response = requests.get(order_url)
                order_response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
                order_data = order_response.json().get("data", {})

                # Get user email
                customer_url = f"{CUSTOMER_SERVICE_URL}/{customer_id}"
                customer_response = requests.get(customer_url)
                customer_response.raise_for_status()
                customer_data = customer_response.json().get("data", {})
                customer_email = customer_data.get("email")
                customer_email = "esdg06t02@gmail.com" # Default email for debugging

                items = order_data.get("items", [])
                formatted_items = "\n".join(
                    [f"- {item['name']} (Quantity: {item['quantity']})" for item in items]
                )  # Adjust field names

                if not customer_email:
                    print(f"No email found for order {order_id}")
                    customer_email = "esdg06t02@gmail.com" # Default email for debugging

                # Customize the email content with fetched order details
                subject = f"Order Confirmation - Order #{order_id}"
                body_text = (
                    f"Dear Customer,\n\n"
                    f"Your order {order_id} has been processed successfully.\n"
                    f"We will deliver your order within 3-5 working days.\n\n"
                    f"Your order:\n{formatted_items}\n\n"
                    f"Thank you for your order!\n"
                )
                email_success = send_email(customer_email, subject, body_text)

            except requests.exceptions.RequestException as e:
                print(f"Failed to fetch order details for order {order_id}: {e}")
                email_success = False  # Failed to send email if order details not fetched

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

    # Declare a queue
    result = channel.queue_declare(queue="", exclusive=True, durable=True)
    queue_name = result.method.queue
    print(f"Queue '{queue_name}' declared")

    # Bind the queue to multiple routing keys
    routing_keys = [
        "delivery.assigned",
        "delivery.pickedup",
        "delivery.delivered",
        "delivery.received",
        "order.payment_success",  # Added routing key for order payment success
    ]
    for routing_key in routing_keys:
        channel.queue_bind(
            exchange=RABBITMQ_EXCHANGE, queue=queue_name, routing_key=routing_key
        )
        print(f"Queue bound to exchange with routing key '{routing_key}'")

    # Set QoS - don't give more than one message to a worker at a time
    channel.basic_qos(prefetch_count=1)

    # Set up consumer
    channel.basic_consume(queue=queue_name, on_message_callback=process_message)

    print(f"Starting consumer, listening for messages on {queue_name}...")
    channel.start_consuming()


if __name__ == "__main__":
    try:
        start_consumer()
    except KeyboardInterrupt:
        print("Consumer stopped by user")
    except Exception as e:
        print(f"Consumer stopped due to error: {e}")