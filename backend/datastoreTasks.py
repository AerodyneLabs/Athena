from datetime import datetime, timedelta
import gridfs
from backend.celery import app
from backend.mongoTask import MongoTask


@app.task(base=MongoTask)
def downloadSounding(modelRun, forecastHours):
    modelTime = datetime.utcfromtimestamp(modelRun)
    fileprefix = 'http://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/'
    filedir = 'gfs.{year:04d}{month:02d}{day:02d}{run:02d}/'.format(
        year=modelTime.year,
        month=modelTime.month,
        day=modelTime.day,
        run=modelTime.hour
    )
    filename = 'gfs.{run:02d}.pgrbf{hour:02d}.grib2'.format(
        run=modelTime.hour,
        hour=forecastHours
    )
    soundingTime = modelTime + timedelta(hours=forecastHours)
    savename = '{year:04d}-{month:02d}-{day:02d}-{hour:02d}'.format(
        year=soundingTime.year,
        month=soundingTime.month,
        day=soundingTime.day,
        hour=soundingTime.hour
    )
    db = downloadSounding.mongo.soundings
    fs = gridfs.GridFS(database=db, collection='files')
    handle = fs.put(fileprefix + filedir + filename, filename=savename)
    return str(handle)
