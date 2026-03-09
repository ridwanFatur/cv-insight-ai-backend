from rabbitmq.constants import CV_REVIEW_TASKS
from utils.config import RABBITMQ_HOST, RABBITMQ_PASS, RABBITMQ_PORT, RABBITMQ_USER
import pika

RABBITMQ_URL = f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_HOST}:{RABBITMQ_PORT}/"

params = pika.URLParameters(RABBITMQ_URL)
connection = pika.BlockingConnection(params)
mq_channel_publisher = connection.channel()

mq_channel_publisher.queue_declare(queue=CV_REVIEW_TASKS, durable=True)
