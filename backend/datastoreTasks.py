from datetime import datetime
from backend.celery import app

@app.task
def downloadSounding(modelRun, forecastHours):
  modelTime = datetime.utcfromtimestamp(modelRun)
  filename = '{0:04d}-{1:02d}-{2:02d}-{3:02d}z-{4:03d}h'.format(
    modelTime.year, modelTime.month, modelTime.day,
    modelTime.hour, forecastHours
  )
  return filename

@app.task
def processSounding(filename):
  print 'Processed: {}'.format(filename)
