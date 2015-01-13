import json
from datetime import datetime
from time import mktime


class CeleryEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return {
                '__type__': '__datetime__',
                'epoc': int(mktime(obj.timetuple()))
                }
        else:
            return json.JSONEncoder.default(self, obj)


def celery_decoder(obj):
    if '__type__' in obj:
        if obj['__type__'] == '__datetime__':
            return datetime.fromtimestamp(obj['epoc'])
    return obj


def celery_dumps(obj):
    return json.dumps(obj, cls=CeleryEncoder)


def celery_loads(obj):
    return json.loads(obj, object_hook=celery_decoder)
