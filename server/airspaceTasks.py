from datetime import date
from math import floor
from requests import get
from zipfile import ZipFile
from collections import namedtuple
from datetime import datetime
from os import remove
from worker import app
from mongoTask import MongoTask


TEMP_DIR = 'data/'
RecordField = namedtuple('RecordField', ['start', 'length', 'just'])
nav_fields = {
    'record': RecordField(1, 4, 'l'),
    'id': RecordField(5, 4, 'l'),
    'type': RecordField(9, 20, 'l'),
    'valid': RecordField(33, 10, 'l'),
    'name': RecordField(43, 30, 'l'),
    'city': RecordField(73, 40, 'l'),
    'state': RecordField(113, 30, 'l'),
    'country': RecordField(148, 30, 'l'),
    'common': RecordField(280, 1, 'l'),
    'public': RecordField(281, 1, 'l'),
    'latitude': RecordField(372, 14, 'l'),
    'longitude': RecordField(397, 14, 'l'),
    'elevation': RecordField(473, 7, 'r'),
    'variation': RecordField(480, 5, 'r'),
    'epoch': RecordField(485, 4, 'r'),
    'status': RecordField(767, 30, 'l'),
}
nav_filter = ['VOR/DME', 'VORTAC']


def get_field(record, field):
    value = record[field.start-1:field.start+field.length-1]
    if field.just == 'l':
        return value.rstrip()
    elif field.just == 'r':
        return value.strip()
    else:
        return value


def parse_dms(x):
    tokens = x.split('-')
    deg = float(tokens[0])
    min = float(tokens[1])
    sec = float(tokens[2][:-1])
    dec = 1.0
    if tokens[2][-1] in ['S', 'W']:
        dec = -1.0
    return (deg + (min / 60) + (sec / 3600)) * dec


def parse_variation(x):
    deg = float(x[:-1])
    if x[-1] == 'E':
        return deg
    else:
        return -deg


def parse_boolean(x):
    if x in ['y', 'Y']:
        return True
    else:
        return False


def get_latest_date():
    # Find latest date on the 56 day cycle
    ref_ord = date(2014, 5, 29).toordinal()
    cur_ord = date.today().toordinal()
    seq = int(floor((cur_ord - ref_ord) / 56))
    latest = date.fromordinal(seq * 56 + ref_ord)
    return latest


def get_latest_url():
    prefix = 'https://nfdc.faa.gov/webContent/56DaySub/'
    folder = '{0}/'.format(get_latest_date())
    return prefix + folder + 'NAV.zip'


@app.task(bind=True)
def download_latest_nav(self):
    # Get file url
    url = get_latest_url()
    filename = url.split('/')[-1]
    # Download file
    request = get(url, stream=True)
    total_length = request.headers.get('content-length')
    cur_length = 0
    if request.status_code == 200:
        with open(TEMP_DIR + filename, 'wb') as file:
            for chunk in request.iter_content(2**18):
                file.write(chunk)
                cur_length += len(chunk)
                self.update_state(
                    state='DOWNLOADING',
                    meta={'current': cur_length, 'total': total_length}
                )
    # Return filename
    return TEMP_DIR + filename


@app.task(base=MongoTask, bind=True)
def process_nav_file(self, filename):
    # Open input zip file
    zf = ZipFile(filename)
    # Open the contained file
    nav_file = zf.open('NAV.txt')
    # Open database collection
    store = process_nav_file.mongo.airspace.navaids
    # Iterate over the file
    count = 0
    for line in nav_file:
        if get_field(line, nav_fields['record']) == 'NAV1':
            type = get_field(line, nav_fields['type'])
            if type in nav_filter:
                try:
                    navaid = {'type': type}
                    navaid['id'] = get_field(line, nav_fields['id'])
                    navaid['valid'] = datetime.strptime(
                        get_field(line, nav_fields['valid']),
                        '%m/%d/%Y')
                    navaid['name'] = get_field(line, nav_fields['name'])
                    navaid['city'] = get_field(line, nav_fields['city'])
                    navaid['state'] = get_field(line, nav_fields['state'])
                    navaid['country'] = get_field(line, nav_fields['country'])
                    navaid['common'] = parse_boolean(get_field(
                        line, nav_fields['common']))
                    navaid['public'] = parse_boolean(get_field(
                        line, nav_fields['public']))
                    lat = parse_dms(get_field(line, nav_fields['latitude']))
                    lon = parse_dms(get_field(line, nav_fields['longitude']))
                    navaid['loc'] = {
                        'type': 'Point',
                        'coordinates': [lon, lat]
                    }
                    navaid['elevation'] = float(get_field(
                        line, nav_fields['elevation']))
                    navaid['variation'] = parse_variation(get_field(
                        line, nav_fields['variation']))
                    navaid['status'] = get_field(line, nav_fields['status'])
                    store.update(
                        {'id': navaid['id']}, {'$set': navaid}, upsert=True)
                    count += 1
                    self.update_state(
                        state='PROCESSING',
                        meta={'current': count}
                    )
                except ValueError:
                    continue
    # Close and delete the zip file
    zf.close()
    remove(filename)
    # Return record count
    return count
