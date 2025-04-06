#!/usr/bin/env python3

"""
A standalone script to create exchanges and queues on RabbitMQ.
"""

import pika
import time

amqp_host = "rabbitmq"
amqp_port = 5672
exchange_name = "notification_topic"
exchange_type = "topic"


def create_exchange(hostname, port, exchange_name, exchange_type):
    print(f"Connecting to AMQP broker {hostname}:{port}...")
    # connect to the broker
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=hostname,
            port=port,
            heartbeat=0,
            blocked_connection_timeout=300,
        )
    )
    print("Connected")

    print("Open channel")
    channel = connection.channel()

    # Set up the exchange if the exchange doesn't exist
    print(f"Declare exchange: {exchange_name}")
    channel.exchange_declare(
        exchange=exchange_name, exchange_type=exchange_type, durable=True
    )
    # 'durable' makes the exchange survive broker restarts

    return channel


def create_queue(channel, exchange_name, queue_name, routing_key, args=None):
    print(f"Bind to queue: {queue_name}")
    channel.queue_declare(queue=queue_name, durable=True, arguments=args)
    # 'durable' makes the queue survive broker restarts

    # bind the queue to the exchange via the routing_key
    channel.queue_bind(
        exchange=exchange_name, queue=queue_name, routing_key=routing_key
    )

dlq_args={
    "x-dead-letter-exchange": "delivery_cancellation_topic",
    "x-dead-letter-routing-key": "dlq",
    "x-message-ttl": 60000,
}
while True:
    try:
        # notification exchange
        channel = create_exchange(
            hostname=amqp_host,
            port=amqp_port,
            exchange_name=exchange_name,
            exchange_type=exchange_type,
        )

        channel = create_exchange(
            hostname=amqp_host,
            port=amqp_port,
            exchange_name="delivery_cancellation_topic",
            exchange_type="topic",
        )


        # Both order payment success and delivery notifications will use the same queue
        create_queue(
            channel=channel,
            exchange_name=exchange_name,
            queue_name="notification_queue",
            routing_key="order.payment_success", # change to notification.email if you want to test notification_service.py
        )
        create_queue(
            channel=channel,
            exchange_name=exchange_name,
            queue_name="notification_queue",
            routing_key="delivery.*", # change to notification.email if you want to test notification_service.py
        )

        # FOR DELIVERY CANCELLATION
        # channel.queue_delete(queue='delivery_cancellation_queue')
        create_queue(
            channel=channel,
            exchange_name="delivery_cancellation_topic",
            queue_name="dlq",
            routing_key="dlq",
        )

        create_queue(
            channel=channel,
            exchange_name="delivery_cancellation_topic",
            queue_name="delivery_cancellation_pending_queue",
            routing_key="delivery_cancellation.pending",
            args=dlq_args,
        )

        create_queue(
            channel=channel,
            exchange_name="delivery_cancellation_topic",
            queue_name="delivery_cancellation_general_queue",
            routing_key="delivery_cancellation.success",
        )

        create_queue(
            channel=channel,
            exchange_name="delivery_cancellation_topic",
            queue_name="delivery_cancellation_general_queue",
            routing_key="delivery_cancellation.escalated",
        )
        

        break
    except pika.exceptions.AMQPConnectionError:
        print("AMQP connection error. Retrying in 10 seconds...")
        time.sleep(10)       
        continue

