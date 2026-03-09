from rabbitmq.constants import CV_REVIEW_TASKS
from utils.config import RABBITMQ_HOST, RABBITMQ_PASS, RABBITMQ_PORT, RABBITMQ_USER
import pika

RABBITMQ_URL = f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_HOST}:{RABBITMQ_PORT}/"

params = pika.URLParameters(RABBITMQ_URL)
connection = pika.BlockingConnection(params)
mq_channel_publisher = connection.channel()

mq_channel_publisher.queue_declare(queue=CV_REVIEW_TASKS, durable=True)


def get_mq_channel_publisher():
    global connection
    global mq_channel_publisher

    if connection.is_closed:
        connection = pika.BlockingConnection(params)
        mq_channel_publisher = connection.channel()

    return mq_channel_publisher
