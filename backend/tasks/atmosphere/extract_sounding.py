from worker import app
from tasks.mongoTask import MongoTask
from datetime import datetime
import gridfs
import numpy as np
from .helpers import generate_sounding


def transform_lon(lon):
    while lon < 0:
        lon += 360
    while lon >= 360:
        lon -= 360
    return lon


@app.task(base=MongoTask, bind=True)
def extract_block(self, time, lat, lon, delta):
    # Convert time if required
    if not isinstance(time, datetime):
        time = datetime.strptime(
            time.split('.')[0],
            '%Y-%m-%dT%H:%M:%S'
        )

    # Generate bounds
    minLat = max(lat - delta, -90)
    maxLat = min(lat + delta, 90)
    minLon = lon - delta
    maxLon = lon + delta

    # Generate lat/lon points
    lats = np.arange(minLat, maxLat + 1, 1)
    lons = np.arange(minLon, maxLon + 1, 1)
    lons = map(transform_lon, lons)

    # Get raw data
    fs = gridfs.GridFS(extract_block.mongo.atmosphere)
    grid_out = fs.get_last_version(forecast=time)
    npz = np.load(grid_out)

    # Get data arrays
    lat_val = npz['lat']
    lon_val = npz['lon']
    u_val = npz['u']
    v_val = npz['v']
    t_val = npz['t']
    h_val = npz['h']
    p_val = npz['p']

    # Extract information
    store = extract_block.mongo.atmosphere.forecast
    ids = []
    for y in lats:
        for x in lons:
            i = len(lat_val) - np.searchsorted(lat_val[::-1], y) - 1
            j = np.searchsorted(lon_val, x)
            tLon = lon_val[j]
            if tLon > 180:
                tLon -= 360
            sounding = generate_sounding(
                analysis=grid_out.analysis,
                forecast=grid_out.forecast,
                lat=lat_val[i],
                lon=tLon,
                height=h_val[:, i, j],
                pressure=p_val[:],
                temperature=t_val[:, i, j],
                u=u_val[:, i, j],
                v=v_val[:, i, j]
            )
            id = store.update({
                    'loc.coordinates': [tLon, lat_val[i]],
                    'forecast': grid_out.forecast
                }, sounding,
                upsert=True
            )
            ids.append(str(id))

    return ids


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
