import amqp_lib
class RabbitMQManager:
    connection = None
    channel = None
    
    @staticmethod
    def start(rabbit_host, rabbit_port, exchange_name, exchange_type):

        print("  Connecting to AMQP broker...")
        try:
            RabbitMQManager.connection, RabbitMQManager.channel = amqp_lib.connect(
                    hostname=rabbit_host,
                    port=rabbit_port,
                    exchange_name=exchange_name,
                    exchange_type=exchange_type,
            )
        except Exception as exception:
            print(f"  Unable to connect to RabbitMQ.\n     {exception=}\n")
            exit(1) # terminate


    

