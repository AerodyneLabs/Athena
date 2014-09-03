from calendar import timegm
from datetime import timedelta
from requests import get
from math import floor
from sounding import Sounding


class Atmosphere:
    GRID_RES = 0.5
    TEMP_RES = 3
    store = {}

    def __init__(self, method='nearest'):
        self.method = method

    def download_sounding(self, time, lat, lon):
        server = 'http://beta.aerodynelabs.com:8080/'
        resource = 'api/sounding/'
        query = '{0}/{1}/{2}'.format(
            timegm(time.timetuple()) * 1000,
            lat, lon
        )
        url = server + resource + query
        r = get(url)
        sounding = Sounding(r.json())
        if sounding.forecast not in self.store:
            self.store[sounding.forecast] = {}
        time_store = self.store[sounding.forecast]
        if sounding.latitude not in time_store:
            time_store[sounding.latitude] = {}
        time_store[sounding.latitude][sounding.longitude] = sounding
        return sounding

    def get_sounding(self, time, lat, lon):
        if time in self.store:
            if lat in self.store[time]:
                if lon in self.store[time][lat]:
                    return self.store[time][lat][lon]
        return self.download_sounding(time, lat, lon)

    def bound_time(self, time):
        x = time.replace(
            minute=0,
            second=0,
            microsecond=0
        )
        extra = time.hour % self.TEMP_RES
        neg = timedelta(hours=extra)
        pos = timedelta(hours=self.TEMP_RES - extra)
        return [x - neg, x + pos]

    def round_location(self, loc):
        min_loc = floor(loc / self.GRID_RES) * self.GRID_RES
        if loc < 0.0:
            max_loc = min_loc
            min_loc = max_loc - self.GRID_RES
        else:
            max_loc = min_loc + self.GRID_RES
        return min_loc, max_loc

    def bound_location(self, lat, lon):
        min_lat, max_lat = self.round_location(lat)
        min_lon, max_lon = self.round_location(lon)
        return [
            [min_lon, min_lat],
            [max_lon, min_lat],
            [max_lon, max_lat],
            [min_lon, max_lat]
        ]

    @staticmethod
    def nearest(point, points):
        if abs(point - points[0]) < abs(point - points[1]):
            return points[0]
        else:
            return points[1]

    def get(self, time, lat, lon, alt):
        time_bounds = self.bound_time(time)
        loc_bounds = self.bound_location(lat, lon)
        if self.method == 'nearest':
            sounding = self.get_sounding(
                Atmosphere.nearest(time, time_bounds),
                Atmosphere.nearest(lat, [loc_bounds[0][1], loc_bounds[2][1]]),
                Atmosphere.nearest(lon, [loc_bounds[0][0], loc_bounds[2][1]])
            )
        return sounding
