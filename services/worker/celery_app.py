import os

from celery import Celery, _state

celery_app = Celery(
    "worker",
    broker=os.getenv("CELERY_BROKER_URL", "amqp://guest:guest@rabbitmq:5672//"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0"),
)

# Set as default app for shared_task
_state.set_default_app(celery_app)

# Autodiscover tasks from the services.worker package
# This allows Celery to find all tasks.py files in the worker package
celery_app.autodiscover_tasks(["services.worker"], force=True)
