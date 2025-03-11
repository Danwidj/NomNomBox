import json
from aiokafka import AIOKafkaProducer
import asyncio

KAFKA_BROKER_URL = "localhost:9092"
KAFKA_TOPIC = "driver-schedule-updates"
PRODUCER_CLIENT_ID = "flask_producer_async"

# Ensure message is in the proper format before sending to Kafka
def serializer(message):
    return json.dumps(message).encode()

# Asynchronous Kafka producer initialization
async def create_producer():
    producer = AIOKafkaProducer(
        bootstrap_servers=KAFKA_BROKER_URL,
        client_id=PRODUCER_CLIENT_ID,
        value_serializer=serializer
    )
    await producer.start()
    return producer

# Async function to send a message to Kafka
async def produce_kafka_message(message):
    producer = await create_producer()
    try:
        # Send the message asynchronously
        await producer.send_and_wait(KAFKA_TOPIC, {'message': message})
    except Exception as e:
        print(f"Failed to send message: {e}")
    finally:
        await producer.stop()


