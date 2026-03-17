from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from jose import jwt, JWTError
from app.config import settings
from app.websocket.connection_manager import manager

router = APIRouter()

@router.websocket("/ws/monitor")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str = Query(None)
):
    # Validate token if provided
    if token:
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )
            user_id = payload.get("sub")
            if user_id is None:
                await websocket.close(code=1008)
                return
        except JWTError:
            await websocket.close(code=1008)
            return
    
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
