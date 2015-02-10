from helpers import download_latest_file, get_field, parse_dms, RecordField
from worker import app
from tasks.mongoTask import MongoTask
from zipfile import ZipFile
from shapely.geometry import Polygon, mapping
import geojson
from os import remove


aff_fields = {
    'record_type': RecordField(1, 4, 'l'),
    'facility_id': RecordField(5, 4, 'l'),
    'name': RecordField(9, 40, 'l'),
    'location': RecordField(49, 30, 'l'),
    'facility_type': RecordField(129, 5, 'l'),
    'state_name': RecordField(144, 30, 'l'),
    'state_code': RecordField(174, 2, 'l'),
    'latitude': RecordField(176, 14, 'l'),
    'longitude': RecordField(201, 14, 'l')
}


arb_fields = {
    'record_id': RecordField(1, 12, 'l'),
    'center_name': RecordField(13, 40, 'l'),
    'structure': RecordField(53, 10, 'l'),
    'latitude': RecordField(63, 14, 'l'),
    'longitude': RecordField(77, 14, 'l'),
    'description': RecordField(91, 300, 'l'),
    'seq_num': RecordField(391, 6, 'l'),
    'nas': RecordField(397, 1, 'l')
}


@app.task(base=MongoTask, bind=True)
def update_centers(self):
    # Create data array
    data = {}

    # Download facility file
    aff_fn = download_latest_file('AFF.zip')
    # Open facility file
    zf = ZipFile(aff_fn)
    aff_file = zf.open('AFF.txt')
    # Process facility file
    for line in aff_file:
        line_type = get_field(line, aff_fields['record_type'])
        if line_type == 'AFF1':
            facility_type = get_field(line, aff_fields['facility_type'])
            if facility_type == 'ARTCC':
                facility_id = get_field(line, aff_fields['facility_id'])
                facility_name = get_field(line, aff_fields['name'])
                location = get_field(line, aff_fields['location'])
                state = get_field(line, aff_fields['state_code'])
                lat = parse_dms(get_field(line, aff_fields['latitude']))
                lon = parse_dms(get_field(line, aff_fields['longitude']))
                data[facility_id] = geojson.Feature(
                    properties={
                        'name': facility_name,
                        'city': location,
                        'state': state,
                        'loc': geojson.Point([lon, lat])
                    },
                    id=facility_id
                )
    # Clean up facility file
    zf.close()
    remove(aff_fn)

    # Download boundary file
    arb_fn = download_latest_file('ARB.zip')
    # Open boundary file
    zf = ZipFile(arb_fn)
    arb_file = zf.open('ARB.txt')
    # Process boundary file
    cur_facility = ''
    cur_alt = ''
    cur_points = []
    poly = None
    for line in arb_file:
        rec_id = get_field(line, arb_fields['record_id'])
        facility_id = rec_id.split(' ')[0]
        rec_alt = get_field(line, arb_fields['structure'])
        if cur_facility != facility_id or cur_alt != rec_alt:
            if cur_facility != '':
                if cur_alt == 'HIGH':
                    cur_points.append(cur_points[0])
                    poly = Polygon(cur_points).buffer(0)
                    data[cur_facility]['geometry'] = mapping(poly)
            cur_facility = facility_id
            cur_alt = rec_alt
            cur_points = []
        lat = parse_dms(get_field(line, arb_fields['latitude']))
        lon = parse_dms(get_field(line, arb_fields['longitude']))
        cur_points.append((lon, lat))
    # Clean up boundary file
    zf.close()
    remove(arb_fn)

    # Open database collection
    store = update_centers.mongo.airspace.artcc
    # Iterate over data
    count = 0
    for id in data:
        rec = data[id]
        if rec.geometry:
            count += 1
            record = rec
            record['_id'] = record.pop('id')
            store.update(
                {'_id': id}, {'$set': record}, upsert=True)
    # Return meaningful result
    return count
