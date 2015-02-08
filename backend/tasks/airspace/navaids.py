from helpers import *
from worker import app
from tasks.mongoTask import MongoTask
from zipfile import ZipFile
from datetime import datetime
import geojson
from os import remove


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


@app.task(base=MongoTask, bind=True)
def update_navaids(self):
    # Download latest file
    filename = download_latest_file('NAV.zip')
    # Open input zip file
    zf = ZipFile(filename)
    # Open the contained file
    nav_file = zf.open('NAV.txt')
    # Open database collection
    store = update_navaids.mongo.airspace.navaid
    # Iterate over the file
    count = 0
    for line in nav_file:
        if get_field(line, nav_fields['record']) == 'NAV1':
            type = get_field(line, nav_fields['type'])
            if type in nav_filter:
                try:
                    properties = {'type': type}
                    id = get_field(line, nav_fields['id'])
                    properties['valid'] = datetime.strptime(
                        get_field(line, nav_fields['valid']),
                        '%m/%d/%Y')
                    properties['name'] = get_field(
                        line, nav_fields['name'])
                    properties['city'] = get_field(
                        line, nav_fields['city'])
                    properties['state'] = get_field(
                        line, nav_fields['state'])
                    properties['country'] = get_field(
                        line, nav_fields['country'])
                    properties['common'] = parse_boolean(get_field(
                        line, nav_fields['common']))
                    properties['public'] = parse_boolean(get_field(
                        line, nav_fields['public']))
                    lat = parse_dms(get_field(
                        line, nav_fields['latitude']))
                    lon = parse_dms(get_field(
                        line, nav_fields['longitude']))
                    properties['elevation'] = 0.3048 * float(get_field(
                        line, nav_fields['elevation']))
                    point = geojson.Point((lon, lat))
                    properties['variation'] = parse_variation(get_field(
                        line, nav_fields['variation']))
                    properties['status'] = get_field(
                        line, nav_fields['status'])
                    navaid = geojson.Feature(
                        geometry=point, properties=properties, id=id)
                    record = navaid
                    record['_id'] = record.pop('id')
                    store.update(
                        {'_id': id}, {'$set': record}, upsert=True)
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
