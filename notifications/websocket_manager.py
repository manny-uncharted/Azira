from fastapi import WebSocket, HTTPException


MAX_CONNECTIONS_PER_ACCOUNT = 3

class ConnectionManager:
    

    def __init__(self):
        self.active_connections: dict = {}
        self.available_tokens: set = set() 

    async def connect(self, websocket: WebSocket, username: str):
        if self.active_connections.get(username, None) and len(self.active_connections[username]) >= MAX_CONNECTIONS_PER_ACCOUNT:
            await websocket.close(code=1008)  # Close connection with policy violation error
            return False
        await websocket.accept()
        if not self.active_connections.get(username):
            self.active_connections[username] = []
        self.active_connections[username].append({
            "websocket": websocket,
            "subscriptions": set()
        })
        return True
    def update_available_tokens(self, token: str):
        self.available_tokens.add(token)

    def is_token_available(self, token: str) -> bool:
        return token in self.available_tokens

    def disconnect(self, websocket: WebSocket, username: str):
        if self.active_connections.get(username):
            self.active_connections[username] = [
                connection for connection in self.active_connections[username]
                if connection["websocket"] != websocket
            ]
            if not self.active_connections[username]:
                del self.active_connections[username]

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def send_error_message(self, message:str):
        for username, connections in self.active_connections.items():
            for connection in connections:
                    await connection["websocket"].send_text(message)

    async def broadcast_to_subscribers(self, token: str, message: str):
        for username, connections in self.active_connections.items():
            for connection in connections:
                if token in connection["subscriptions"]:
                    await connection["websocket"].send_text(message)

manager = ConnectionManager()