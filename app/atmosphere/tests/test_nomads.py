from collections import namedtuple
from datetime import datetime, timedelta
from unittest.mock import patch
from django.test import TestCase
import nose.tools
import pytz
import requests

import atmosphere.tasks.nomads as nomads

class NOMADSTestCase(TestCase):

    def test_previous_model(self):
        t = datetime(2015, 7, 31, 5)
        nose.tools.assert_equal(nomads.previous_model(t), datetime(2015, 7, 31, 0))

    def test_conservative_previous_model(self):
        t = datetime(2015, 7, 31, 5)
        nose.tools.assert_equal(nomads.previous_model(t, conservative=True), datetime(2015, 7, 30, 18))

    def test_previous_forecast(self):
        mt = datetime(2015, 7, 31, 6)
        ft = datetime(2015, 7, 31, 10)
        nose.tools.assert_equal(nomads.previous_forecast(mt, ft), datetime(2015, 7, 31, 9))

    def test_previous_forecast_max(self):
        mt = datetime(2015, 7, 31, 6)
        ft = datetime(2015, 8, 11, 10)
        nose.tools.assert_equal(nomads.previous_forecast(mt, ft), datetime(2015, 8, 10, 6))

    def test_gfs_url_naive_model(self):
        mt = datetime(2015, 7, 31, 6)
        ft = datetime(2015, 7, 31, 9)
        nose.tools.assert_raises(ValueError, nomads.gfs_url, mt, ft)

    def test_gfs_url_naive_forecast(self):
        mt = datetime(2015, 7, 31, 6, tzinfo=pytz.utc)
        ft = datetime(2015, 7, 31, 9)
        nose.tools.assert_raises(ValueError, nomads.gfs_url, mt, ft)

    def test_gfs_url_early_forecast(self):
        mt = datetime(2015, 7, 31, 6)
        ft = datetime(2015, 7, 31, 5)
        nose.tools.assert_raises(ValueError, nomads.gfs_url, mt, ft)

    def test_gfs_url_invalid_resolution(self):
        mt = datetime(2015, 7, 31, 6)
        ft = datetime(2015, 7, 31, 9)
        nose.tools.assert_raises(ValueError, nomads.gfs_url, mt, ft, -1)

    def test_gfs_url_future_model(self):
        mt = datetime.now(tz=pytz.utc) + timedelta(hours=6)
        ft = datetime.now(tz=pytz.utc) + timedelta(hours=12)
        nose.tools.assert_raises(ValueError, nomads.gfs_url, mt, ft)

    def test_gfs_url_one_degree(self):
        mt = datetime(2015, 7, 31, 6, tzinfo=pytz.utc)
        ft = datetime(2015, 7, 31, 9, tzinfo=pytz.utc)
        url = nomads.gfs_url(model_run=mt, forecast_time=ft, resolution=nomads.GFS_1_0_DEGREE)
        nose.tools.assert_equal(url, 'http://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.2015073106/gfs.t06z.pgrb2.1p00.f003')

    def test_gfs_url_half_degree(self):
        mt = datetime(2015, 7, 31, 6, tzinfo=pytz.utc)
        ft = datetime(2015, 7, 31, 9, tzinfo=pytz.utc)
        url = nomads.gfs_url(model_run=mt, forecast_time=ft, resolution=nomads.GFS_0_5_DEGREE)
        nose.tools.assert_equal(url, 'http://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.2015073106/gfs.t06z.pgrb2.0p50.f003')

    def test_gfs_url_quarter_degree(self):
        mt = datetime(2015, 7, 31, 6, tzinfo=pytz.utc)
        ft = datetime(2015, 7, 31, 9, tzinfo=pytz.utc)
        url = nomads.gfs_url(model_run=mt, forecast_time=ft, resolution=nomads.GFS_0_25_DEGREE)
        nose.tools.assert_equal(url, 'http://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.2015073106/gfs.t06z.pgrb2.0p25.f003')

    def test_get_index_fail(self):
        mt = datetime(2015, 7, 31, 6, tzinfo=pytz.utc)
        ft = datetime(2015, 7, 31, 9, tzinfo=pytz.utc)
        url = nomads.gfs_url(model_run=mt, forecast_time=ft) + '.fail'
        nose.tools.assert_raises(RuntimeError, nomads._get_index, url)

    @patch('requests.get')
    def test_get_index(self, mock):
        # Create mock requests.get
        RequestResponse = namedtuple('RequestResponse', ['status_code', 'text'])
        response = RequestResponse(200,
            """1:0:d=2015073106:UGRD:planetary boundary layer:anl:
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
        nose.tools.assert_equal(index[4], nomads.IndexRecord(5, 190581, 'd=2015073106', 'HGT', '10 mb', 'anl', ''))
