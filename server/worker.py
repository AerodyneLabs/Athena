from __future__ import absolute_import
from celery import Celery
from kombu.serialization import register
import serializer


register(
    'myjson',
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
        'datastoreTasks'
    ]
)

app.conf.update(
    CELERY_ENABLE_UTC=True,
    CELERY_RESULT_SERIALIZER='myjson',
    CELERY_ACCEPT_CONTENT=['myjson'],
    CELERY_TASK_SERIALIZER='myjson',
    CELERY_TRACK_STARTED=True,
    CELERY_TASK_RESULT_EXPIRES=3600
)

if __name__ == '__main__':
    app.start()
