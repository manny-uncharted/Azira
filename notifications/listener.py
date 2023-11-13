import zmq
import asyncio
import logging
from notifications.websocket_manager import manager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def zmq_listener():
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://localhost:5556")
    socket.setsockopt_string(zmq.SUBSCRIBE, '')  # Subscribe to all messages initially

    while True:
        try:
            message = await asyncio.to_thread(socket.recv_string)
            # Log received message
            # logger.info(f"Received message from ZeroMQ: {message}")
            token, data = message.split(' & ')
            manager.update_available_tokens(token)
            await manager.broadcast_to_subscribers(token, data)
        except zmq.Again:
            # No message was available, wait shortly and try again
            logger.info("No message was available, wait shortly and try again")
            await manager.send_error_message("No message was available, wait shortly and try again later")
            await asyncio.sleep(0.01)
        except Exception as e:
            logger.error(f"Error in zmq_listener: {e}")
            await asyncio.sleep(1)  # Prevent a tight loop on continuous error