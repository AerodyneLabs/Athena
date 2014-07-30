from requests import get
from datetime import datetime
from worker import app


TEMP_PREFIX = 'data/temp/'


def get_url(model_run, forecast_hours):
    server_address = 'http://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/'
    model_folder = 'gfs.{year:04d}{month:02d}{day:02d}{run:02d}/'.format(
        year=model_run.year,
        month=model_run.month,
        day=model_run.day,
        run=model_run.hour
    )
    forecast_file = 'gfs.t{run:02d}z.pgrbf{forecast:02d}.grib2'.format(
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


@app.task()
def download_sounding(modelRun, forecastHours):
    # Get datetime object from modelRun timestamp
    model_time = datetime.utcfromtimestamp(modelRun)

    # Download the sounding
    savename = download_forecast(model_time, forecastHours)

    return str(savename)
