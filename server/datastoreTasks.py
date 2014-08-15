from requests import get
from datetime import datetime, timedelta
from worker import app
from pygrib import open as grib
from mongoTask import MongoTask
import gridfs
import numpy as np
from os import remove


TEMP_DIR = 'data/'


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


def generate_sounding(
        lat=None, lon=None,
        height=None, pressure=None, temperature=None, u=None, v=None,
        **kwargs):
    sounding = {
        'loc': {
            'type': 'Point',
            'coordinates': [lon, lat]
        },
        'data': []
    }
    for h, p, t, u, v in zip(height, pressure, temperature, u, v):
        sounding['data'].append({
            'h': h, 'p': p, 't': t, 'u': u, 'v': v
        })

    return dict(kwargs.items() + sounding.items())


@app.task(base=MongoTask, bind=True)
def extract_forecast(self, time_string, lat, lon):
    # Convert time string to datetime object
    forecast_time = datetime.strptime(time_string, '%Y-%m-%dT%H:%M:%S')
    # Get GridFS
    fs = gridfs.GridFS(extract_forecast.mongo.atmosphere)
    # Get npz from grid
    grid_out = fs.get_last_version(forecast=forecast_time)
    # Load npz and get values
    npz = np.load(grid_out)
    lats = npz['lat']
    lons = npz['lon']
    u_val = npz['u']
    v_val = npz['v']
    t_val = npz['t']
    h_val = npz['h']
    p_val = npz['p']
    # Find array indicies
    nLat = lats.shape[0]
    i = -np.searchsorted(lats[::-1], lat) + nLat - 1
    j = np.searchsorted(lons, lon)

    # Extract information
    soundings = []
    try:
        for i, j in zip(lat, lon):
            soundings.append(generate_sounding(
                analysis=grid_out.analysis.isoformat(),
                forecast=grid_out.forecast.isoformat(),
                lat=lats[i], lon=lons[j],
                height=h_val[:, i, j],
                pressure=p_val[:],
                temperature=t_val[:, i, j],
                u=u_val[:, i, j],
                v=v_val[:, i, j]
            ))
    except TypeError:
        soundings.append(generate_sounding(
            analysis=grid_out.analysis.isoformat(),
            forecast=grid_out.forecast.isoformat(),
            lat=lats[i], lon=lons[j],
            height=h_val[:, i, j],
            pressure=p_val[:],
            temperature=t_val[:, i, j],
            u=u_val[:, i, j],
            v=v_val[:, i, j]
        ))

    # Return soundings
    return soundings


@app.task(base=MongoTask, bind=True)
def download_forecast(self, model_run, forecast_hours):
    # Convert time string to datetime object
    analysis_time = datetime.strptime(model_run, '%Y-%m-%dT%H:%M:%S')
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
    npz_file_name = process_file(TEMP_DIR + file_name)
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

    # Clean up temporary files
    remove(TEMP_DIR + file_name)
    remove(npz_file_name)

    # Return the file name
    return npz_file_name
