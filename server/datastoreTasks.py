from datetime import datetime, timedelta
from requests import get
import pygrib
from numpy import asscalar
from backend.celery import app
from backend.mongoTask import MongoTask


def get_url(model_run, forecast_hours):
    server_address = 'http://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/'
    model_folder = 'gfs.{year:04d}{month:02d}{day:02d}{run:02d}/'.format(
        year=model_run.year,
        month=model_run.month,
        day=model_run.day,
        run=model_run.hour
    )
    forecast_file = 'gfs.t{run:02d}z.pgrbf{hour:02d}.grib2'.format(
        run=model_run.hour,
        forecast=forecast_hours
    )
    return server_address + model_folder + forecast_file


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

    # Extract data from sounding
    print 'Opening file: ' + savename
    file = pygrib.open('data/temp/' + savename)
    lat, lon = file[1].latlons()

    # Save sounding in database
    store = download_sounding.mongo.soundings.forecast
    for y in range(len(lat)):
        print '{0} - {1}'.format(savename, asscalar(lat[y]))
        for x in range(len(lon)):
            coords = [asscalar(lon[x]), asscalar(lat[y])]
            query = {
                'time': soundingTime,
                'loc': {
                    'type': 'Point',
                    'coordinates': coords
                }
            }
            sounding = {'$set': {
                'model': modelTime
            }}
            store.update(query, sounding, upsert=True)

    return str(savename)
