from requests import get
from datetime import datetime, timedelta
from worker import app
from pygrib import open as grib
from mongoTask import MongoTask
import gridfs


TEMP_PREFIX = 'data/temp/'


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
    file_url = get_url(model_run, forecast_hours)
    forecast_time = model_run + timedelta(hours=forecast_hours)
    file_name = model_run.strftime('%Y%m%d%H') + '-' + forecast_time.strftime('%Y%m%d%H') + '.grib2'
    db = download_forecast.mongo.atmosphere
    fs = gridfs.GridFS(db)
    request = get(file_url, stream=True)
    if request.status_code == 200:
        with fs.new_file(filename=file_name, analysis=model_run,
                forecast=forecast_time) as file:
            for chunk in request.iter_content(1024):
                file.write(chunk)
    return TEMP_PREFIX + file_name


@app.task(base=MongoTask)
def process_file(file_name):
    # Select the database collection
    store = process_file.mongo.atmosphere.forecast

    # Open grib file
    print 'Opening file...'
    file = grib(file_name)

    # Extract common information
    print 'Extracting common info...'
    analysis_time = file[1].analDate
    valid_time = file[1].validDate
    lats = file[1].distinctLatitudes
    lons = file[1].distinctLongitudes

    # Select relevant records
    print 'Selecting records...'
    u_sel = file.select(shortName='u', typeOfLevel='isobaricInhPa')
    v_sel = file.select(shortName='v', typeOfLevel='isobaricInhPa')
    t_sel = file.select(shortName='t', typeOfLevel='isobaricInhPa')
    h_sel = file.select(shortName='gh', typeOfLevel='isobaricInhPa')

    # Iterate over data
    print 'Iterating...'
    for i, lat in enumerate(lats):
        # Ignore extreme latitudes
        if abs(lat) > 75:
            continue

        for j, lon in enumerate(lons):
            # Generate query document
            query = {
                'forecast': valid_time,
                'loc': {
                    'type': 'Point',
                    'coordinates': [lon, lat]
                }
            }
            # Generate forecast body
            body = {
                'analysis': analysis_time,
                'data': []
            }
            # Iterate over levels
            for level in range(len(u_sel)):
                p = u_sel[level].level * 100
                u = u_sel[level].values[i, j]
                v = v_sel[level].values[i, j]
                t = t_sel[level].values[i, j]
                h = h_sel[level].values[i, j]
                body['data'].append({'h': h, 'p': p, 't': t, 'u': u, 'v': v})

            # Save to db
            print 'Processed: {0}, {1}'.format(lat, lon)
            store.update(query, {'$set': body}, upsert=True)


@app.task(base=MongoTask)
def get_forecast(modelRun, forecastHours):
    # Get datetime object from modelRun timestamp
    model_time = datetime.utcfromtimestamp(modelRun)

    # Download the sounding
    print 'Downloading...'
    savename = download_forecast(model_time, forecastHours)

    # Process the sounding
    print 'Processing...'
    process_file(savename, download_sounding.mongo)

    return str(savename)
