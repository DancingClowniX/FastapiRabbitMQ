import os
import time
import pika
from dotenv import load_dotenv

QUEUE_NAME = "test_queue"

load_dotenv()

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")


def callback(ch, method, properties, body):
    print(f" [Consumer] Поймал сообщение: '{body.decode()}'", flush=True)


print(" [Consumer] Ожидание подключения к RabbitMQ...")
while True:
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=RABBITMQ_HOST)
        )
        channel = connection.channel()
        channel.queue_declare(queue=QUEUE_NAME,durable=True)

        channel.basic_consume(
            queue=QUEUE_NAME, on_message_callback=callback, auto_ack=True
        )

        print(" [Consumer] Успешно подключено! Жду сообщения...", flush=True)
        channel.start_consuming()
    except pika.exceptions.AMQPConnectionError:
        time.sleep(2)