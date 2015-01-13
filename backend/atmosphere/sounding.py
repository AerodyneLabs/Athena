from datetime import datetime
import numpy as np


class Sounding:

    def __init__(self, data):
        self.analysis = self.parse_timestring(data['analysis'])
        self.forecast = self.parse_timestring(data['forecast'])
        self.latitude = float(data['loc']['coordinates'][1])
        self.longitude = float(data['loc']['coordinates'][0])
        self.data = np.zeros(
            len(data['data']),
            dtype=[
                ('h', 'f8'),
                ('p', 'f8'),
                ('t', 'f8'),
                ('u', 'f8'),
                ('v', 'f8')
            ]
        )
        for i, x in enumerate(data['data']):
            self.data[i] = (
                x['h'], x['p'], x['t'], x['u'], x['v']
            )
        self.data.sort(order=['h'])
        self.delta = np.zeros_like(self.data)
        self.compute()

    @staticmethod
    def parse_timestring(ts):
        return datetime.strptime(
            ts.split('.')[0], '%Y-%m-%dT%H:%M:%S')

    def compute(self):
        for i in range(len(self.data) - 1):
            x0 = self.data[i]
            x1 = self.data[i + 1]
            dh = x1['h'] - x0['h']
            dp = (x1['p'] - x0['p']) / dh
            dt = (x1['t'] - x0['t']) / dh
            du = (x1['u'] - x0['u']) / dh
            dv = (x1['v'] - x0['v']) / dh
            self.delta[i] = (dh, dp, dt, du, dv)

    def find_base(self, alt):
        low = 0
        hi = len(self.data) - 1
        if alt < self.data[low]['h']:
            return low
        if alt >= self.data[hi]['h']:
            return hi
        while (hi - low) > 1:
            mid = int((low + hi) / 2)
            if alt >= self.data[mid]['h']:
                low = mid
            else:
                hi = mid
        return low

    def get(self, alt):
        base_idx = self.find_base(alt)
        base = self.data[base_idx]
        delta = self.delta[base_idx]
        dh = alt - base['h']
        return {
            'h': alt,
            'p': delta['p'] * dh + base['p'],
            't': delta['t'] * dh + base['t'],
            'u': delta['u'] * dh + base['u'],
            'v': delta['v'] * dh + base['v']
        }
