import os
import time
import pika
from dotenv import load_dotenv
from faststream.rabbit import  RabbitBroker
from faststream import FastStream

import asyncio

QUEUE_NAME = "my_queue"

load_dotenv()



broker = RabbitBroker(os.getenv('RABBITMQ_URL'))
app = FastStream(broker)


print(" [Consumer] Ожидание подключения к RabbitMQ...")
@broker.subscriber("my_queue")
async def handle_message(msg: dict):
    # Этот код сработает автоматически, как только в очередь прилетит сообщение
    print(f" [x] Получено сообщение из очереди: {msg}")

if __name__ == "__main__":
    asyncio.run(app.run())
