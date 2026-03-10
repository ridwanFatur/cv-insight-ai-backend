import json

import pika

from rabbitmq.constants import CV_REVIEW_TASKS
from rabbitmq.channel_publisher import get_mq_channel_publisher


def cv_review_publish(cv_feedback_id, user_id, file_link):
    channel = get_mq_channel_publisher()
    channel.basic_publish(
        exchange='',
        routing_key=CV_REVIEW_TASKS,
        body=json.dumps({
            "id": cv_feedback_id,
            "user_id": user_id,
            "file_link": file_link,
        }),
        properties=pika.BasicProperties(
            delivery_mode=2,
        )
    )
