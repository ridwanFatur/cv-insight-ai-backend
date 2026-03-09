import json


def cv_review_callback(ch, method, properties, body):
    data = json.loads(body)
    print("Received:", data)

    ch.basic_ack(delivery_tag=method.delivery_tag)
