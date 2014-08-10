from requests import get
from datetime import datetime, timedelta
from worker import app
from pygrib import open as grib
from mongoTask import MongoTask
import gridfs


def get_url(model_run, forecast_hours):
    server_address = 'http://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/'
    model_folder = 'gfs.{year:04d}{month:02d}{day:02d}{run:02d}/'.format(
        year=model_run.year,
        month=model_run.month,
        day=model_run.day,
        run=model_run.hour
    )
    forecast_file = 'gfs.t{run:02d}z.pgrb2f{forecast:02d}'.format(
        run=model_run.hour,
        forecast=forecast_hours
    )
    return server_address + model_folder + forecast_file


@app.task(base=MongoTask)
def download_forecast(model_run, forecast_hours):
    # Get URL of file on web
    file_url = get_url(model_run, forecast_hours)
    # Compute forecast datetime
    forecast_time = model_run + timedelta(hours=forecast_hours)
    # Determine human readable file name
    file_name = model_run.strftime('%Y%m%d%H') + '-' + forecast_time.strftime('%Y%m%d%H') + '.grib2'
    # Get GridFS instance
    fs = gridfs.GridFS(download_forecast.mongo.atmosphere)
    # Download the file and save to GridFS
    request = get(file_url, stream=True)
    if request.status_code == 200:
        with fs.new_file(filename=file_name, analysis=model_run,
                forecast=forecast_time) as file:
            for chunk in request.iter_content(1024):
                file.write(chunk)
    # Return the file name
    return file_name


