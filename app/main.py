from fastapi import FastAPI
import asyncio
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from middleware.middleware import ProcessTimeMiddleware #, DBSessionMiddleware

from routes import users, trigger_router
from notifications.messaging_bq import zmqConn

origins = [
    "*"
]

app = FastAPI(debug=True)
zmq_server = zmqConn()

@app.on_event("startup")
async def startup_event():
    await zmq_server._zmq_config(5556)
    asyncio.create_task(zmq_server.load_data())
    asyncio.create_task(zmq_server.server_setup("5556"))

@app.on_event("shutdown")
async def shutdown_event():
    await zmq_server.stop()


@app.get('/health')
def send_response():
    return {"response": "OKay"}

app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# app.add_middleware(DBSessionMiddleware)
app.add_middleware(ProcessTimeMiddleware)

app.include_router(users.router, prefix="/api/v1/users")
app.include_router(trigger_router.trigger)

