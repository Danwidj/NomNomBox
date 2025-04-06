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
import logging
from datetime import datetime, timezone, timedelta

load_dotenv()  # Load environment variables from .env file

# RabbitMQ connection details
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")  # or esd-rabbit once on docker
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", "5672"))
RABBITMQ_EXCHANGE = os.getenv("RABBITMQ_EXCHANGE", "notification_topic")
NOTIFICATIONS_QUEUE = os.getenv("NOTIFICATIONS_QUEUE", "notification_queue") # get Notifications queue name

# Email configuration
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SENDER_EMAIL = os.getenv("SENDER_EMAIL", SMTP_USERNAME)

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
        logging.info(f"Email sent successfully to {recipient_email}")
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
            customer_email = data.get("customer_email") # Email!
            # Get user email

            subject = f"Payment Successful - Order #{order_id}"
            body_text = f"""
                Hi there,

                🎉 Your Meal Kit Order #{order_id} is confirmed! 🎉

                We're excited to let you know that your payment was successful. Thank you so much for choosing NomNomBox! 💖  
                Our team is now preparing your meal kit with the freshest ingredients — made with love. 🥦🥕🍅

                📅 Next Step Required:  
                Please go to your Profile Page and click on the "Orders" tab.  
                From there, select a delivery date for this order so we can schedule it accordingly.

                We’ll keep you updated every step of the way and notify you once your meal kit is out for delivery. 🚚✨

                Thanks again and get ready to say *NomNom*! 😋🍴

                Warm regards,  
                The NomNomBox Team 💌
            """

            if not customer_email:
                print(f"No email address found for customer_id. Skipping.")
                ch.basic_ack(delivery_tag=method.delivery_tag)
                return

            email_success = send_email(customer_email, subject, body_text)
        
        elif routing_key == "delivery.assigned":
        # driver_notification_message = {
        #     "delivery_id": delivery_id,
        #     "name": driver_response["name"],
        #     "email": driver_response["email"],
        #     "location": user_address,
        #     "timeslot": desired_delivery_time,
        #     "status": "Assigned to Driver",
        # }
            delivery_id = data.get("delivery_id")
            driver_name = data.get("name")
            driver_email = data.get("email")
            location = data.get("location")
            timeslot = data.get("timeslot")
            status = data.get("status")
            subject= f"Delivery Assigned - Delivery #{delivery_id}"
            # Define Singapore timezone (UTC+8)
            sg_timezone = timezone(timedelta(hours=8))

            # Convert the Unix timestamp to a datetime object in SG time
            formatted_timeslot = datetime.fromtimestamp(int(timeslot), tz=sg_timezone).strftime('%A, %d %B %Y at %I:%M %p')

            # Use in email body
            body_text = f"""
            Dear {driver_name},
            A delivery with ID {delivery_id} has been assigned to you! 🚚
            Here are the details:
            - Delivery ID: {delivery_id}
            - Location: {location}
            - Timeslot: {formatted_timeslot}
            """
            email_success = send_email(driver_email, subject, body_text)
            if email_success:
                logging.info(f"Email sent successfully to {driver_email}")
            else:
                logging.error(f"Failed to send email to {driver_email}")




        elif routing_key in ( #Change condition of key routing here
            "delivery.pickedup",
            "delivery.delivered",
            "delivery.received",
        ):
            # Process delivery status updates
            delivery_id = data.get("delivery_id")
            status = data.get("status")
            customer_email = data.get("email")  # email - ADDED THE COMMPOSITE!!
            name = data.get("name")  # name - ADDED THE COMMPOSITE!!
            delivery_time = data.get("delivery_time")  #delivery_time - ADDED THE COMMPOSITE!!
            order_id = data.get("order_id")  #order_id - ADDED THE COMMPOSITE!!

            subject = f"Delivery Status Update - Delivery #{order_id}"
            body_text = f"""
            👋 Dear Customer,

            🚚 Exciting news! Your delivery for order #{order_id} has been updated!

            The current status is: {status} 🎉

            We're working hard to get your delicious meal kit to you as quickly as possible. We'll keep you posted on any further updates.

            Thank you for your order! 💖

            Warm regards,

            The NomNomBox Team 📦
            """
            # template = string.Template(DELIVERY_PICKEDUP_TEMPLATE) # set template
            # body_text = template.substitute(delivery_id=delivery_id,status=status)

            if not customer_email:
                print(f"No email address found for delivery_id. Skipping.")
                ch.basic_ack(delivery_tag=method.delivery_tag)
                return

            email_success = send_email(customer_email, subject, body_text)

        else:
            print(f"Unknown routing key: {routing_key}. Skipping.")
            logging.error(f"Unknown routing key: {routing_key}")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return

        if email_success:
            ch.basic_ack(delivery_tag=method.delivery_tag)
            print("Message acknowledged")
            logging.info("Message acknowledged and email sent")
        else:
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
            print("Message negative acknowledged (requeued)")

    except json.JSONDecodeError:
        print(f"Invalid JSON in message: {body}")
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"Error processing message: {e}")
        logging.error(f"Error processing message: {e}")
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

    # Actually declare the queue
    result = channel.queue_declare(
        queue=NOTIFICATIONS_QUEUE, durable=True
    )
    queue_name = result.method.queue
    print(f"Queue '{queue_name}' declared. Message count: {result.method.message_count}")

    # Bind the queue to various routing keys
    routing_keys = [
        "order.payment_success",
        "delivery.pickedup",
        "delivery.delivered",
        "delivery.received",
        "delivery.assigned"
    ]
    
    for key in routing_keys:
        channel.queue_bind(
            exchange=RABBITMQ_EXCHANGE,
            queue=queue_name,
            routing_key=key
        )
        print(f"Queue '{queue_name}' bound to exchange with routing key '{key}'")

    channel.basic_qos(prefetch_count=1)
    print("QoS prefetch count set to 1")

    # Set up consumer
    channel.basic_consume(
        queue=queue_name, 
        on_message_callback=process_message
    )

    print(f"Starting consumer, listening for messages on {queue_name}...")
    channel.start_consuming()

if __name__ == "__main__":
    try:
        start_consumer()

    except KeyboardInterrupt:
        print("Consumer stopped by user")
    except Exception as e:
        print(f"Consumer stopped due to error: {e}")