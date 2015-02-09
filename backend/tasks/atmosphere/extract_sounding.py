from worker import app
from tasks.mongoTask import MongoTask
from datetime import datetime
import gridfs
import numpy as np
from .helpers import generate_sounding


@app.task(base=MongoTask, bind=True)
def extract_sounding(self, forecast_time, lat, lon):
    """Extract a given sounding from the database and save it."""
    if not isinstance(forecast_time, datetime):
        forecast_time = datetime.strptime(
            forecast_time.split('.')[0],
            '%Y-%m-%dT%H:%M:%S'
        )
    # Get GridFS
    fs = gridfs.GridFS(extract_sounding.mongo.atmosphere)
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
    store = extract_sounding.mongo.atmosphere.forecast
    soundings = []
    try:
        for i, j in zip(lat, lon):
            sounding = generate_sounding(
                analysis=grid_out.analysis,
                forecast=grid_out.forecast,
                lat=lats[i], lon=lons[j],
                height=h_val[:, i, j],
                pressure=p_val[:],
                temperature=t_val[:, i, j],
                u=u_val[:, i, j],
                v=v_val[:, i, j]
            )
            soundings.append(sounding)
    except TypeError:
        sounding = generate_sounding(
            analysis=grid_out.analysis,
            forecast=grid_out.forecast,
            lat=lats[i], lon=lons[j],
            height=h_val[:, i, j],
            pressure=p_val[:],
            temperature=t_val[:, i, j],
            u=u_val[:, i, j],
            v=v_val[:, i, j]
        )
        soundings.append(sounding)
    finally:
        # Cache soundings
        ids = store.insert(soundings)
        # Return soundings
        return map(lambda o: str(o), ids)
