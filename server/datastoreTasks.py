from datetime import datetime, timedelta
from requests import get
import pygrib
from numpy import asscalar
from backend.celery import app
from backend.mongoTask import MongoTask


TEMP_PREFIX = 'data/temp'


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


def download_forecast(model_run, forecast_hours):
    file_url = get_url(model_run, forecast_hours)
    file_name = file_url.split('/')[-1]
    request = get(file_url, stream=True)
    if request.status_code == 200:
        with open(TEMP_PREFIX + file_name, 'wb') as file:
            for chunk in request.iter_content(1024):
                file.write(chunk)
    return TEMP_PREFIX + file_name


@app.task(base=MongoTask)
def download_sounding(modelRun, forecastHours):
    # Get datetime object from modelRun timestamp
    model_time = datetime.utcfromtimestamp(modelRun)

    # Download the sounding
    savename = download_forecast(model_time, forecastHours)

    # Extract data from sounding
    print 'Opening file: ' + savename
    file = pygrib.open(savename)
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
