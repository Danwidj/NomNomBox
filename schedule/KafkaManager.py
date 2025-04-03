from flask import Flask, request, jsonify
import json
from kafka import KafkaConsumer, KafkaProducer
import traceback
import time
class KafkaManager():
    producer = None
    consumer = None
    @staticmethod
    def start_producer():
        KafkaManager.producer = KafkaProducer(
            bootstrap_servers='kafka:9092', api_version=(2, 6, 0))
        # Get cluster layout and initial topic/partition leadership information
        print("producer abt to start")

    @staticmethod
    def start_kafka_consumer(topic, broker_url):
        while True:  
            try:
                print("Starting Kafka consumer...")
                if KafkaManager.consumer is None:            
                    KafkaManager.consumer = KafkaConsumer(
                        topic,
                        bootstrap_servers=broker_url,
                        group_id="my-group",
                        auto_offset_reset="earliest",
                        heartbeat_interval_ms=1000,
                        api_version=(2, 6, 0)
                    )
                else:
                    print("Kafka consumer already started.")
                    break
  
            except Exception as e:
                print(f"Kafka consumer failed: {e}")
                traceback.print_exc()
                print("Reconnecting in 10 seconds...")
                time.sleep(10)  # Wait before reconnecting