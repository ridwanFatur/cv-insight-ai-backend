import json
import logging

logger = logging.getLogger(__name__)


def cv_review_callback(ch, method, properties, body):
    data = json.loads(body)
    logger.info(f"Received: {data}")

    ch.basic_ack(delivery_tag=method.delivery_tag)
