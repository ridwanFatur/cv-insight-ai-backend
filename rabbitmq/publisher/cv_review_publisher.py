import json

import pika

from rabbitmq.constants import CV_REVIEW_TASKS
from rabbitmq.publisher import mq_channel_publisher


def cv_review_publish(user_id, file_uri):
    mq_channel_publisher.basic_publish(
        exchange='',
        routing_key=CV_REVIEW_TASKS,
        body=json.dumps({
            "file_uri": file_uri,
            "user_id": user_id
        }),
        properties=pika.BasicProperties(
            delivery_mode=2,
        )
    )
