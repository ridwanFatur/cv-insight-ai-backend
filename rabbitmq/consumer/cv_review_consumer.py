import json
import logging
from utils.connection_manager import ws_manager
import asyncio
logger = logging.getLogger(__name__)
MAIN_LOOP = asyncio.get_event_loop()


def cv_review_callback(ch, method, properties, body):
    data = json.loads(body)
    logger.info(f"Received: {data}")
    user_id = data["user_id"]
    cv_id = data["id"]
    type = data["type"]
    if type == "cv_updated":
        feedback = data["feedback"]
        payload = {"id": cv_id, "status": "finished", "feedback": feedback}
        asyncio.run_coroutine_threadsafe(
            ws_manager.send_to_user(user_id, json.dumps(payload)),
            MAIN_LOOP
        )

    ch.basic_ack(delivery_tag=method.delivery_tag)
