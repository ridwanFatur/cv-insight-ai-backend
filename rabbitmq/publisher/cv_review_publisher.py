import json

import pika

from rabbitmq.constants import CV_REVIEW_TASKS
from rabbitmq.channel_publisher import get_mq_channel_publisher, mq_channel_publisher


def cv_review_publish(cv_feedback_id):
    channel = get_mq_channel_publisher()
    channel.basic_publish(
        exchange='',
        routing_key=CV_REVIEW_TASKS,
        body=json.dumps({
            "id": cv_feedback_id,
        }),
        properties=pika.BasicProperties(
            delivery_mode=2,
        )
    )
