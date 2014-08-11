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


def process_file(input_name):
    # Open grib file
    grib_file = grib(input_name)
    # Select records from grib file
    u_sel = grib_file.select(shortName='u', typeOfLevel='isobaricInhPa')
    v_sel = grib_file.select(shortName='v', typeOfLevel='isobaricInhPa')
    t_sel = grib_file.select(shortName='t', typeOfLevel='isobaricInhPa')
    h_sel = grib_file.select(shortName='gh', typeOfLevel='isobaricInhPa')
    # Extract values from records
    vals = lambda x: x.values
    u_val = map(vals, u_sel)
    v_val = map(vals, v_sel)
    t_val = map(vals, t_sel)
    h_val = map(vals, h_sel)
    p_val = map(lambda x: x.level * 100, u_sel)
    lats = u_sel[0].distinctLatitudes
    lons = u_sel[0].distinctLongitudes
    # Close input file
    grib_file.close()

    # Determine output file name
    output_name = input_name.split('.')[0] + '.npz'
    # Save values to output file
    np.savez_compressed(
        output_name,
        h=h_val,
        p=p_val,
        t=t_val,
        u=u_val,
        v=v_val,
        lat=lats,
        lon=lons
    )

    # Return output file name
    return output_name


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


