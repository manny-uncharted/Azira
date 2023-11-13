from celery import Celery
from notifications.websocket_manager import manager
from asgiref.sync import async_to_sync
from celery.utils.log import get_task_logger

# Update broker URL to use Redis
notifier = Celery("notifier", broker="redis://localhost:6379/0", backend="redis://localhost:6379/0")

celery_log = get_task_logger(__name__)

@notifier.task
def notification(message: dict):
    message_status = async_to_sync(manager.send_personal_message)(message)
    return message_status
