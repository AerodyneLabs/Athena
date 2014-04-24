from datetime import datetime
import gridfs
from backend.celery import app
from backend.mongoTask import MongoTask

@app.task(base=MongoTask)
def downloadSounding(modelRun, forecastHours):
  modelTime = datetime.utcfromtimestamp(modelRun)
  filename = '{0:04d}-{1:02d}-{2:02d}-{3:02d}z-{4:03d}h'.format(
    modelTime.year, modelTime.month, modelTime.day,
    modelTime.hour, forecastHours
  )
  db = downloadSounding.mongo.soundings
  fs = gridfs.GridFS(db)
  handle = fs.put(filename, filename=filename)
  print fs.get(handle)
  return str(handle)
