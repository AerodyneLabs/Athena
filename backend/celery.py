from __future__ import absolute_import
from celery import Celery

app = Celery(
  'backend',
  broker='amqp://',
  backend='amqp',
  include=[
    'backend.datastoreTasks'
  ]
)

app.conf.update(
  CELERY_ENABLE_UTC=True,
  CELERY_RESULT_SERIALIZER='json',
  CELERY_TASK_RESULT_EXPIRES=3600,
  CELERY_ACCEPT_CONTENT = ['json'],
  CELERY_TRACK_STARTED=True,
  CELERY_TASK_SERIALIZER='json',
)

if __name__ == '__main__':
  app.start()
