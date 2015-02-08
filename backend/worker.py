from __future__ import absolute_import
from celery import Celery
from kombu.serialization import register
from tasks import serializer


register(
    'json',
    serializer.celery_dumps,
    serializer.celery_loads,
    content_type='application/json',
    content_encoding='utf-8'
)

app = Celery(
    'backend',
    broker='amqp://',
    backend='amqp',
    include=[
        'tasks.airspaceTasks',
        'tasks.atmosphereTasks'
    ]
)

app.conf.update(
    CELERY_ENABLE_UTC=True,
    CELERY_RESULT_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_TASK_SERIALIZER='json',
    CELERY_TRACK_STARTED=True,
    CELERY_TASK_RESULT_EXPIRES=3600
)

if __name__ == '__main__':
    app.start()
