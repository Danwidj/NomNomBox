from flask import Flask, request, jsonify
import json
from kafka import KafkaProducer
import logging
class KafkaManager():
    producer = None
    @staticmethod
    def start_producer():
        KafkaManager.producer = KafkaProducer(
            bootstrap_servers='kafka:9092', api_version=(2, 6, 0))
        # Get cluster layout and initial topic/partition leadership information
        logging.info("Kafka producer started.")


    # @staticmethod
    # def publish_message(message, kafka_topic):
    #     try:
    #         if KafkaManager.producer is None:
    #             KafkaManager.start_producer()
    #         # Get the message from the request
    #         message = request.json
    #         message = json.dumps(message).encode()
            
    #         if not message:
    #             return jsonify({"error": "Invalid message format"}), 400

    #         KafkaManager.producer.send(KAFKA_TOPIC, value=message)

    #         # Return success response
    #         return jsonify({"message": "Message sent"}), 200
    #     except Exception as e:
    #         # Handle any errors
    #         return jsonify({"error": str(e)}), 500