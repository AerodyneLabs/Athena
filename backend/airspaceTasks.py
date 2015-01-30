from datetime import date
from math import floor
from requests import get
from zipfile import ZipFile
from collections import namedtuple
from datetime import datetime
from os import remove
from shapefile import Reader
from geojson import Feature, Point, Polygon
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
nav_filter = ['VOR/DME', 'VORTAC']
airspace_files = {
    'Shape_Files/class_b': 'Class B',
    'Shape_Files/class_c': 'Class C',
    'Shape_Files/class_d': 'Class D'
}


def get_field(record, field):
    """Return the contents of a field from the record as a string."""
    # Extract field based on start position and length
    value = record[field.start-1:field.start+field.length-1]
    # Strip white space based on justification
    if field.just == 'l':
        return value.rstrip()
    elif field.just == 'r':
        return value.strip()
    else:
        return value


def parse_dms(x):
    """Return a float representation of a dd-mm-ss.ssH string."""
    # Split the string into tokens
    tokens = x.split('-')
    # Convert string tokens to floats
    deg = float(tokens[0])
    min = float(tokens[1])
    sec = float(tokens[2][:-1])
    # Parse the hemisphere value
    dec = 1.0
    if tokens[2][-1] in ['S', 'W']:
        dec = -1.0
    return (deg + (min / 60) + (sec / 3600)) * dec


def parse_variation(x):
    """Return a float representation of a ddH string."""
    # Convert degrees to float
    deg = float(x[:-1])
    # Parse the hemisphere value
    if x[-1] == 'E':
        return deg
    else:
        return -deg


def parse_boolean(x):
    """Return a boolean representation of a y/n string."""
    if x in ['y', 'Y']:
        return True
    else:
        return False


def get_latest_date():
    """Return the latest date on the 56 day update cycle."""
    # Reference date
    ref_ord = date(2014, 5, 29).toordinal()
    # Current date
    cur_ord = date.today().toordinal()
    # Compute cycles since reference
    seq = int(floor((cur_ord - ref_ord) / 56))
    # Convert cycles back to date
    latest = date.fromordinal(seq * 56 + ref_ord)
    return latest


def get_latest_url(filename):
    """Return the root URL of NFDC file server for latest cycle."""
    prefix = 'https://nfdc.faa.gov/webContent/56DaySub/'
    folder = '{0}/'.format(get_latest_date())
    return prefix + folder + filename


def download_latest_file(filename):
    # Get file url
    url = get_latest_url(filename)
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
    # Return filename
    return TEMP_DIR + filename


@app.task(base=MongoTask, bind=True)
def process_artcc(self):
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
                data[facility_id] = Feature(properties={
                    'name': facility_name,
                    'city': location,
                    'state': state,
                    'loc': Point([lon, lat])
                }, id=facility_id)
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
                    poly = Polygon([cur_points])
                    data[cur_facility]['geometry'] = poly
            cur_facility = facility_id
            cur_alt = rec_alt
            cur_points = []
        lat = parse_dms(get_field(line, arb_fields['latitude']))
        lon = parse_dms(get_field(line, arb_fields['longitude']))
        cur_points.append((lon, lat))
    #Clean up boundary file
    zf.close()
    remove(arb_fn)

    # Open database collection
    store = process_artcc.mongo.airspace.artcc
    # Iterate over data
    count = 0
    for id in data:
        rec = data[id]
        if rec.geometry:
            count += 1
            store.update(
                {'id': rec.id}, {'$set': rec}, upsert=True)
    # Return meaningful result
    return count


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
                    point = Point((lon, lat))
                    properties['elevation'] = float(get_field(
                        line, nav_fields['elevation']))
                    properties['variation'] = parse_variation(get_field(
                        line, nav_fields['variation']))
                    properties['status'] = get_field(
                        line, nav_fields['status'])
                    navaid = Feature(
                        geometry=point, properties=properties, id=id)
                    store.update(
                        {'id': id}, {'$set': navaid}, upsert=True)
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


@app.task(base=MongoTask, bind=True)
def process_airspace_file(self, filename):
    # Open input zip file
    zf = ZipFile(filename)
    # Open the database
    store = process_airspace_file.mongo.airspace.airspaces
    store.remove()
    # Iterate different airspace types
    count = 0
    for airspace_name, airspace_class in airspace_files.iteritems():
        # Extract component files
        shp_fn = zf.extract(airspace_name + '.shp', TEMP_DIR)
        shx_fn = zf.extract(airspace_name + '.shx', TEMP_DIR)
        dbf_fn = zf.extract(airspace_name + '.dbf', TEMP_DIR)
        # Open interface to shapefile
        sf = Reader(shp_fn)
        # Iterate over shapes
        for sr in sf.shapeRecords():
            id = sr.record[1]
            loAlt = 0
            if sr.record[2] != 'SFC':
                try:
                    loAlt = float(sr.record[2])
                except ValueError:
                    pass
            hiAlt = float(sr.record[3])
            bbox = sr.shape.bbox
            bounds = Polygon([[
                (bbox[0], bbox[1]),
                (bbox[2], bbox[1]),
                (bbox[2], bbox[3]),
                (bbox[0], bbox[3]),
                (bbox[0], bbox[1])
            ]])
            feature = Feature(
                geometry=sr.shape,
                id=id,
                properties={
                    'airspace': sr.record[0],
                    'lo': loAlt,
                    'hi': hiAlt,
                    'class': airspace_class
                },
                bounds=bounds
            )
            store.insert(feature)
            count += 1
            self.update_state(
                state='PROCESSING',
                meta={'current': count}
            )
        # Delete the temp files
        remove(shp_fn)
        remove(shx_fn)
        remove(dbf_fn)
    # Close/delete zip file
    zf.close()
    remove(filename)
    # Return something useful
    return count
