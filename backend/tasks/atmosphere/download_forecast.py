from worker import app
from tasks.mongoTask import MongoTask
from .helpers import get_url
from datetime import timedelta
from requests import get
from .process_forecast import process_forecast
import gridfs
from os import remove


TEMP_DIR = 'data/'


@app.task(base=MongoTask, bind=True)
def download_forecast(self, analysis_time, forecast_hours):
    """Download a forecast and store it as a compressed numpy file."""
    # Get URL of file on web
    file_url = get_url(analysis_time, forecast_hours)
    # Compute forecast datetime
    forecast_time = analysis_time + timedelta(hours=forecast_hours)
    # Determine human readable file name
    file_name = analysis_time.strftime('%Y%m%d%H') + '-' + \
        forecast_time.strftime('%Y%m%d%H') + '.grib2'
    # Download the file and save to temp file
    request = get(file_url, stream=True)
    total_length = request.headers.get('content-length')
    cur_length = 0
    if request.status_code == 200:
        with open(TEMP_DIR + file_name, 'wb') as file:
            for chunk in request.iter_content(2**18):
                file.write(chunk)
                cur_length += len(chunk)
                self.update_state(
                    state='DOWNLOADING',
                    meta={'current': cur_length, 'total': total_length}
                )

    # Extract data into compressed file
    self.update_state(state='PROCESSING')
    npz_file_name = process_forecast(TEMP_DIR + file_name)
    # Get GridFS
    fs = gridfs.GridFS(download_forecast.mongo.atmosphere)
    # Save compressed file to GridFS
    self.update_state(state='SAVING')
    npz_file = open(npz_file_name, 'rb')
    fs.put(
        npz_file,
        analysis=analysis_time,
        forecast=forecast_time
    )
    npz_file.close()

    # Clear forecast cache
    store = download_forecast.mongo.atmosphere.forecast
    store.remove({'forecast': forecast_time})

    # Clean up temporary files
    remove(TEMP_DIR + file_name)
    remove(npz_file_name)

    # Return the file name
    return npz_file_name
