

def get_url(model_run, forecast_hours):
    """Return the URL for the given forecast of the given model run."""
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


def generate_sounding(
        lat=None, lon=None,
        height=None, pressure=None, temperature=None, u=None, v=None,
        **kwargs):
    """Return a sounding object generated from the input data."""
    sounding = {
        'loc': {
            'type': 'Point',
            'coordinates': [lon, lat]
        },
        'profile': []
    }
    for h, p, t, u, v in zip(height, pressure, temperature, u, v):
        sounding['profile'].append({
            'h': h, 'p': p, 't': t, 'u': u, 'v': v
        })

    return dict(kwargs.items() + sounding.items())
