from datetime import datetime, timedelta
from gridfs import GridFS
from requests import get
from backend.celery import app
from backend.mongoTask import MongoTask


@app.task(base=MongoTask)
def download_sounding(modelRun, forecastHours):
    # Get datetime object from modelRun timestamp
    modelTime = datetime.utcfromtimestamp(modelRun)

    # Generate the url for the requested sounding
    fileprefix = 'http://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/'
    filedir = 'gfs.{year:04d}{month:02d}{day:02d}{run:02d}/'.format(
        year=modelTime.year,
        month=modelTime.month,
        day=modelTime.day,
        run=modelTime.hour
    )
    filename = 'gfs.t{run:02d}z.pgrbf{hour:02d}.grib2'.format(
        run=modelTime.hour,
        hour=forecastHours
    )
    soundingTime = modelTime + timedelta(hours=forecastHours)

    # Create a human readable filename for the sounding
    savename = '{year:04d}-{month:02d}-{day:02d}-{hour:02d}.grib2'.format(
        year=soundingTime.year,
        month=soundingTime.month,
        day=soundingTime.day,
        hour=soundingTime.hour
    )

    # Download the sounding
    print 'Saving file: ' + savename
    r = get(fileprefix + filedir + filename, stream=True)
    if r.status_code == 200:
        with open('data/temp/' + savename, 'wb') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)

    #db = downloadSounding.mongo.soundings
    #fs = GridFS(database=db, collection='files')
    #handle = fs.put(fileprefix + filedir + filename, filename=savename)
    return str(savename)
