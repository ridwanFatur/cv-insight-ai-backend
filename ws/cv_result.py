from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from utils.connection_manager import verify_websocket_token, ws_manager
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/ws/cv-result",
    tags=["cv-result"]
)


@router.websocket("/{user_id}")
async def cv_result(websocket: WebSocket, user_id: int):
    payload = await verify_websocket_token(websocket, user_id)
    if not payload:
        return
    await ws_manager.connect(user_id, websocket)

    try:
        while True:
            data = await websocket.receive_text()
            logger.info(f"Websocket: {data}")
    except WebSocketDisconnect:
        ws_manager.disconnect(user_id)
