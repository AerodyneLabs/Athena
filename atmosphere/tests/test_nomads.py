from datetime import datetime, timedelta
from types import SimpleNamespace
from unittest.mock import patch
from django.test import TestCase
import nose.tools
import pytz
import requests

import atmosphere.tasks.nomads as nomads

class Previous(TestCase):

    def setUp(self):
        self.model = datetime(2015, 7, 31, 5, tzinfo=pytz.utc)
        self.real_model = datetime(2015, 7, 31, 6, tzinfo=pytz.utc)

    def test_previous_model(self):
        nose.tools.assert_equal(nomads.previous_model(self.model), datetime(2015, 7, 31, 0, tzinfo=pytz.utc))

    def test_previous_model_conservative(self):
        nose.tools.assert_equal(nomads.previous_model(self.model, conservative=True), datetime(2015, 7, 30, 18, tzinfo=pytz.utc))

    def test_previous_forecast(self):
        ft = datetime(2015, 7, 31, 10, tzinfo=pytz.utc)
        nose.tools.assert_equal(nomads.previous_forecast(self.real_model, ft), datetime(2015, 7, 31, 9, tzinfo=pytz.utc))

    def test_previous_forecast_max(self):
        ft = datetime(2015, 8, 11, 10, tzinfo=pytz.utc)
        nose.tools.assert_equal(nomads.previous_forecast(self.real_model, ft), datetime(2015, 8, 10, 6, tzinfo=pytz.utc))

class GfsUrl(TestCase):

    def setUp(self):
        self.naive_model = datetime(2015, 7, 31, 6)
        self.naive_forecast = datetime(2015, 7, 31, 9)
        self.model = datetime(2015, 7, 31, 6, tzinfo=pytz.utc)
        self.forecast = datetime(2015, 7, 31, 9, tzinfo=pytz.utc)
        self.early_forecast = datetime(2015, 7, 31, 5, tzinfo=pytz.utc)

    def test_naive_model(self):
        nose.tools.assert_raises(ValueError, nomads.gfs_url, self.naive_model, self.forecast)

    def test_naive_forecast(self):
        nose.tools.assert_raises(ValueError, nomads.gfs_url, self.model, self.naive_forecast)

    def test_early_forecast(self):
        nose.tools.assert_raises(ValueError, nomads.gfs_url, self.model, self.early_forecast)

    def test_invalid_resolution(self):
        nose.tools.assert_raises(ValueError, nomads.gfs_url, self.model, self.forecast, -1)

    def test_future_model(self):
        mt = datetime.now(tz=pytz.utc) + timedelta(hours=6)
        ft = datetime.now(tz=pytz.utc) + timedelta(hours=12)
        nose.tools.assert_raises(ValueError, nomads.gfs_url, mt, ft)

    def test_one_degree(self):
        url = nomads.gfs_url(model_run=self.model, forecast_time=self.forecast, resolution=nomads.GFS_1_0_DEGREE)
        nose.tools.assert_equal(url, 'http://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.2015073106/gfs.t06z.pgrb2.1p00.f003')

    def test_half_degree(self):
        url = nomads.gfs_url(model_run=self.model, forecast_time=self.forecast, resolution=nomads.GFS_0_5_DEGREE)
        nose.tools.assert_equal(url, 'http://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.2015073106/gfs.t06z.pgrb2.0p50.f003')

    def test_quarter_degree(self):
        url = nomads.gfs_url(model_run=self.model, forecast_time=self.forecast, resolution=nomads.GFS_0_25_DEGREE)
        nose.tools.assert_equal(url, 'http://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.2015073106/gfs.t06z.pgrb2.0p25.f003')

class Index(TestCase):

    def setUp(self):
        self.index = [
            SimpleNamespace(name='UGRD', level='planetary boundary layer', start_byte=0, stop_byte=53283),
            SimpleNamespace(name='VGRD', level='planetary boundary layer', start_byte=53284, stop_byte=107281),
            SimpleNamespace(name='VRATE', level='planetary boundary layer', start_byte=107282, stop_byte=136872),
            SimpleNamespace(name='GUST', level='surface', start_byte=136873, stop_byte=190580),
            SimpleNamespace(name='HGT', level='10 mb', start_byte=190581, stop_byte=234918),
            SimpleNamespace(name='TMP', level='10 mb', start_byte=234919, stop_byte=256586),
            SimpleNamespace(name='RH', level='10 mb', start_byte=256587, stop_byte=266289),
            SimpleNamespace(name='UGRD', level='10 mb', start_byte=266290, stop_byte=291236),
            SimpleNamespace(name='VGRD', level='10 mb', start_byte=291237, stop_byte=313146),
            SimpleNamespace(name='ABSV', level='10 mb', start_byte=313147, stop_byte=353236),
            SimpleNamespace(name='O3MR', level='10 mb', start_byte=353237, stop_byte=None),
        ]

    def test_bad_index(self):
        mt = datetime(2015, 7, 31, 6, tzinfo=pytz.utc)
        ft = datetime(2015, 7, 31, 9, tzinfo=pytz.utc)
        url = nomads.gfs_url(model_run=mt, forecast_time=ft) + '.fail'
        nose.tools.assert_raises(RuntimeError, nomads._get_index, url)

    @patch('requests.get')
    def test_get_index(self, mock):
        # Create mock requests.get
        response = SimpleNamespace(status_code=200,
            text="""1:0:d=2015073106:UGRD:planetary boundary layer:anl:
            2:53284:d=2015073106:VGRD:planetary boundary layer:anl:
            3:107282:d=2015073106:VRATE:planetary boundary layer:anl:
            4:136873:d=2015073106:GUST:surface:anl:
            5:190581:d=2015073106:HGT:10 mb:anl:
            6:234919:d=2015073106:TMP:10 mb:anl:
            7:256587:d=2015073106:RH:10 mb:anl:
            8:266290:d=2015073106:UGRD:10 mb:anl:
            9:291237:d=2015073106:VGRD:10 mb:anl:
            10:313147:d=2015073106:ABSV:10 mb:anl:
            11:353237:d=2015073106:O3MR:10 mb:anl:""")
        mock.return_value = response
        url = 'http://mock'

        index = nomads._get_index(url)

        mock.assert_called_with(url + '.idx')
        nose.tools.assert_equal(index, self.index)

    def test(self):
        nose.tools.assert_equal(
            nomads._filter_index(self.index, ['VGRD'], ['planetary boundary layer', '10 mb']),
            [self.index[1], self.index[8]]
        )

    def test_no_names(self):
        nose.tools.assert_equal(
            nomads._filter_index(self.index, levels=['planetary boundary layer']),
            [self.index[0], self.index[1], self.index[2]]
        )

    def test_no_levels(self):
        nose.tools.assert_equal(
            nomads._filter_index(self.index, names=['UGRD']),
            [self.index[0], self.index[7]]
        )

    def test_build_range_header(self):
        nose.tools.assert_equal(
            nomads._build_range_header([self.index[0], self.index[10]]),
            'bytes=0-53283,353237-'
        )
