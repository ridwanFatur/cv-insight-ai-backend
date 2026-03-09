import pika
from rabbitmq.constants import CV_REVIEW_RESULTS
from utils.config import RABBITMQ_HOST, RABBITMQ_PASS, RABBITMQ_PORT, RABBITMQ_USER

RABBITMQ_URL = f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_HOST}:{RABBITMQ_PORT}/"

params = pika.URLParameters(RABBITMQ_URL)
connection = pika.BlockingConnection(params)
mq_channel_client = connection.channel()

mq_channel_client.queue_declare(queue=CV_REVIEW_RESULTS, durable=True)
