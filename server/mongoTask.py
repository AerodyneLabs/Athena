from __future__ import absolute_import
from celery import Task
from pymongo import MongoClient


class MongoTask(Task):
    abstract = True
    _mongo = None

    @property
    def mongo(self):
        if self._mongo is None:
            self._mongo = MongoClient()
        return self._mongo
