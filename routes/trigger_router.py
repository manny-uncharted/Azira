from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException
from websockets.exceptions import ConnectionClosedError, ConnectionClosedOK
from sqlalchemy.orm import Session
import zmq
import jwt
import time
import asyncio

#Local imports
from notifications.websocket_manager import manager
from notifications.listener import zmq_listener
from utils.auth_jwt import SECRET_KEY, ALGORITHM
from crud.tokens import get_token_by_user_id
from crud.users import get_user
from middleware.middleware import get_db
from models.users import User
from models.tokens import Token


trigger = APIRouter(prefix="/api/trigger", tags=["trigger_in"])

@trigger.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str, db: Session = Depends(get_db)):
    # Extract the JWT token from the headers
    token = None
    for key, value in websocket.headers.items():
        if key.lower() == "authorization":
            token = value.split(" ")[1]  # Assumes the header is in the format "Bearer <token>"
            break

    if not token:
        await websocket.close(code=1008)
        return
    print(f"Token: {token}")
    db_user = db.query(User).filter(User.username == username).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid username")

    token_user = db.query(Token).filter(Token.access_token == token).first()
    print(f"User token from db: {token_user}")
    if not token_user:
        raise HTTPException(status_code=401, detail="Invalid token")


    # Try to connect and enforce connection limits
    if not await manager.connect(websocket, username):
        return

    try:
        while True:
            data = await websocket.receive_text()
            action, tokens = data.split('|')
            tokens = tokens.split(',')
            
            if action == "subscribe":
                missing_tokens = []
                for token in tokens:
                    # Check if the token is available in the stream (implement this check as needed)
                    if not manager.is_token_available(token):  # You need to implement this function
                        missing_tokens.append(token)
                    else:
                        connection = next((c for c in manager.active_connections[username] if c["websocket"] == websocket), None)
                        if connection:
                            connection["subscriptions"].add(token)

                if missing_tokens:
                    await manager.send_personal_message(f"Tokens not found: {', '.join(missing_tokens)}", websocket)
                    await websocket.close(code=1008)  # Close the connection
                    return
                else:
                    await manager.send_personal_message(f"Subscribed to tokens: {', '.join(tokens)}", websocket)
            
            elif action == "unsubscribe":
                for token in tokens:
                    connection = next((c for c in manager.active_connections[username] if c["websocket"] == websocket), None)
                    if connection:
                        connection["subscriptions"].discard(token)
                await manager.send_personal_message(f"Unsubscribed from tokens: {', '.join(tokens)}", websocket)
            
            else:
                await manager.send_personal_message(f"Unknown action: {action}", websocket)

    except WebSocketDisconnect:
        manager.disconnect(websocket, username)
    except Exception as e:
        await manager.send_personal_message(f"Error: {str(e)}", websocket)
        manager.disconnect(websocket, username)

@trigger.on_event("startup")
async def startup_event():
    asyncio.create_task(zmq_listener())