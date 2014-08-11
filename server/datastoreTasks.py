from requests import get
from datetime import datetime, timedelta
from worker import app
from pygrib import open as grib
from mongoTask import MongoTask
import gridfs
import numpy as np


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


@app.task(base=MongoTask, bind=True)
def download_forecast(self, model_run, forecast_hours):
    # Convert time string to datetime object
    analysis_time = datetime.strptime(model_run, '%Y-%m-%dT%H:%M:%S')
    # Get URL of file on web
    file_url = get_url(analysis_time, forecast_hours)
    # Compute forecast datetime
    forecast_time = analysis_time + timedelta(hours=forecast_hours)
    # Determine human readable file name
    file_name = analysis_time.strftime('%Y%m%d%H') + '-' + forecast_time.strftime('%Y%m%d%H') + '.grib2'
    # Get GridFS instance
    fs = gridfs.GridFS(download_forecast.mongo.atmosphere)
    # Download the file and save to temp file
    request = get(file_url, stream=True)
    total_length = request.headers.get('content-length')
    cur_length = 0
    if request.status_code == 200:
        with open('data/' + file_name, 'wb') as file:
            for chunk in request.iter_content(2**18):
                file.write(chunk)
                cur_length += len(chunk)
                self.update_state(
                    state='DOWNLOADING',
                    meta={'current': cur_length, 'total': total_length}
                )
    # Return the file name
    return file_name


