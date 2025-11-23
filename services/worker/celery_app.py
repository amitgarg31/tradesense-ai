from celery import Celery
from celery import _state
import os

broker_url = f"amqp://{os.getenv('RABBITMQ_DEFAULT_USER')}:{os.getenv('RABBITMQ_DEFAULT_PASS')}@rabbitmq:5672//"
backend_url = f"redis://{os.getenv('REDIS_HOST')}:{os.getenv('REDIS_PORT')}/0"

celery_app = Celery("tradesense", broker=broker_url, backend=backend_url)

# Set as default app for shared_task
_state.set_default_app(celery_app)

# Autodiscover tasks from the services.worker package
# This allows Celery to find all tasks.py files in the worker package
celery_app.autodiscover_tasks(['services.worker'], force=True)