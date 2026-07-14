import os
from dotenv import load_dotenv
import pika

class DataUser:
    __slots__ = ["user","password"]

    def __init__(self,user,password):
        self.user = user
        self.password = password


class RabbitMQService:
    @classmethod
    def init_env(cls):
        load_dotenv()

    def __init__(self):
        self.init_env()
        self.host = os.getenv("RABBITMQ_HOST")
        self.queue_name = "test_queue"
        self._connection = None
        self._channel = None

    def connect(self) -> None:
        if not self._connection or self._connection.is_closed:
            self._connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=self.host)
            )
            self._channel = self._connection.channel()
            self._channel.queue_declare(queue=self.queue_name, durable=True)

    def close(self) -> None:
        if self._connection and self._connection.is_open:
            self._connection.close()
            print(" [Producer] Соединение с RabbitMQ успешно закрыто.")

    def send_message(self, message: str = "Запись") -> None:
        self.connect()
        self._channel.basic_publish(
            exchange="",
            routing_key=self.queue_name,
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=pika.DeliveryMode.Persistent
            )
        )
        print(f" [Producer] Отправлено: '{message}'")