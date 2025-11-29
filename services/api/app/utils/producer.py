import os

from celery import Celery

broker_url = (
    f"amqp://{os.getenv('RABBITMQ_DEFAULT_USER')}:"
    f"{os.getenv('RABBITMQ_DEFAULT_PASS')}@rabbitmq:5672//"
)
backend_url = f"redis://{os.getenv('REDIS_HOST')}:{os.getenv('REDIS_PORT')}/0"

celery = Celery("tradesense", broker=broker_url, backend=backend_url)


def send_to_queue(data):
    celery.send_task("tasks.process_data", args=[data], queue="trades")
