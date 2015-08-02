from datetime import datetime, timedelta
import pytz

GFS_1_0_DEGREE = 0
GFS_0_5_DEGREE = 1
GFS_0_25_DEGREE = 2
GFS_MODEL_TIMESTEP = 6
GFS_FORECAST_TIMESTEP = 3
GFS_FORECAST_MAX = 240
GFS_RESOLUTION = {
    GFS_1_0_DEGREE: '1p00',
    GFS_0_5_DEGREE: '0p50',
    GFS_0_25_DEGREE: '0p25',
}

def gfs_url(model_run=datetime.now(tz=pytz.utc), forecast_time=datetime.now(tz=pytz.utc), resolution=GFS_1_0_DEGREE):
    # Ensure times are not naive
    if model_run.tzinfo is None or model_run.tzinfo.utcoffset(model_run) is None:
        raise ValueError('model_run (%s) is naive!', model_run)
    if forecast_time.tzinfo is None or forecast_time.tzinfo.utcoffset(forecast_time) is None:
        raise ValueError('forecast_time (%s) is naive!', forecast_time)

    # Ensure forecast_time is not before model_run
    if forecast_time < model_run:
        raise ValueError('forecast_time (%s) is before model_run (%s)!', forecast_time, model_run)

    # Ensure resolution is known
    if resolution not in GFS_RESOLUTION:
        raise ValueError('resolution (%s) not valid!', resolution)

    # Ensure model_run is not in the future
    if model_run > datetime.now(tz=pytz.utc):
        raise ValueError('model_run (%s) is in the future!', model_run)

    # Get previous model run time
    model_run = previous_model(model_run)

    # Get previous forecast time
    forecast_time = previous_forecast(model_run, forecast_time)

    # Compute forecast hours
    forecast_hours = int((forecast_time - model_run).total_seconds() // 3600)

    # Generate url fragments
    base_url = 'http://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/'
    model_folder = 'gfs.{year:04d}{month:02d}{day:02d}{hour:02d}/'.format(
        year=model_run.year,
        month=model_run.month,
        day=model_run.day,
        hour=model_run.hour
    )
    forecast_filename = 'gfs.t{run:02d}z.pgrb2.{resolution}.f{forecast:03d}'.format(
        run=model_run.hour,
        resolution=GFS_RESOLUTION[resolution],
        forecast=forecast_hours
    )

    # Return full url
    return base_url + model_folder + forecast_filename

def previous_model(model, conservative=False):
    discard = timedelta(
        hours=model.hour % GFS_MODEL_TIMESTEP,
        minutes=model.minute,
        seconds=model.second,
        microseconds=model.microsecond
    )

    if conservative:
        discard += timedelta(hours=6)

    return model - discard

def previous_forecast(model, forecast):
    # Compute number of hours between model and forecast
    dt = (forecast - model).total_seconds() / 3600
    # Get forecast timestep before requested forecast time
    h = (dt // GFS_FORECAST_TIMESTEP) * GFS_FORECAST_TIMESTEP
    # Limit forecast time to maximum timestep
    if h > GFS_FORECAST_MAX:
        h = GFS_FORECAST_MAX
    # Return forecast timestep time
    return model + timedelta(hours=h)
