from helpers import (
    download_latest_file,
    get_field,
    parse_dms,
    RecordField
)
from worker import app
from tasks.mongoTask import MongoTask
from zipfile import ZipFile
import geojson
from os import remove


twr_fields = {
    'record_type': RecordField(1, 4, 'l'),
    'facility_id': RecordField(5, 4, 'l'),
    'site_number': RecordField(19, 11, 'l'),
    'region': RecordField(30, 3, 'l'),
    'state': RecordField(63, 2, 'l'),
    'city': RecordField(65, 40, 'l'),
    'name': RecordField(105, 50, 'l'),
    'latitude': RecordField(155, 14, 'l'),
    'longitude': RecordField(180, 14, 'l'),
    'fss_id': RecordField(205, 4, 'l'),
    'fss_name': RecordField(209, 30, 'l'),
    'facility_type': RecordField(239, 12, 'l'),
    'operation_hours': RecordField(251, 2, 'l'),
    'operation_regularity': RecordField(253, 3, 'l'),
    'master_id': RecordField(256, 4, 'l'),
    'master_name': RecordField(260, 50, 'l')
}


@app.task(base=MongoTask, bind=True)
def update_towers(self):
    # Init status count
    types = {
        'ATCT': 0,
        'NON-ATCT': 0,
        'ATCT-A/C': 0,
        'ATCT-RAPCON': 0,
        'ATCT-RATCF': 0,
        'ATCT-TRACON': 0,
        'TRACON': 0,
        'ATCT-TRACAB': 0,
        'ATCT-CERAP': 0
    }
    # Get store
    store = update_towers.mongo.airspace.tower
    # Download tower file
    twr_fn = download_latest_file('TWR.zip')
    # Open tower file
    zf = ZipFile(twr_fn)
    twr_file = zf.open('TWR.txt')
    # Process tower file
    for line in twr_file:
        line_type = get_field(line, twr_fields['record_type'])
        if line_type == 'TWR1':
            facility_type = get_field(line, twr_fields['facility_type'])
            facility_id = get_field(line, twr_fields['facility_id'])
            region = get_field(line, twr_fields['region'])
            state = get_field(line, twr_fields['state'])
            city = get_field(line, twr_fields['city'])
            name = get_field(line, twr_fields['name'])
            master_id = get_field(line, twr_fields['master_id'])
            master_name = get_field(line, twr_fields['master_name'])
            lat = parse_dms(get_field(line, twr_fields['latitude']))
            lon = parse_dms(get_field(line, twr_fields['longitude']))
            # Create record
            point = None
            if lat:
                point = geojson.Point((lon, lat))
            properties = {
                'name': name,
                'type': facility_type,
                'region': region,
                'state': state,
                'city': city
            }
            if master_id is not '':
                properties['master'] = {
                    '_id': master_id,
                    'name': master_name
                }
            data = geojson.Feature(
                geometry=point,
                properties=properties,
                id=facility_id
            )
            rec = data
            rec['_id'] = rec.pop('id')
            store.update(
                {'_id': facility_id},
                {'$set': rec},
                upsert=True
            )
            types[facility_type] += 1
    # Cleanup
    zf.close()
    remove(twr_fn)
    # Return useful data
    return types
