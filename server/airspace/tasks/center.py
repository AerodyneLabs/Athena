from celery import shared_task
from celery.utils.log import get_task_logger
from airspace.tasks import helpers
from airspace.models.center import Center
from zipfile import ZipFile
from django.contrib.gis.geos import Point, Polygon, MultiPolygon
from os import remove

logger = get_task_logger(__name__)

AFF_FIELDS = {
    'record_type': helpers.RecordField(1, 4, 'l'),
    'facility_id': helpers.RecordField(5, 4, 'l'),
    'name': helpers.RecordField(9, 40, 'l'),
    'location': helpers.RecordField(49, 30, 'l'),
    'facility_type': helpers.RecordField(129, 5, 'l'),
    'state_name': helpers.RecordField(144, 30, 'l'),
    'state_code': helpers.RecordField(174, 2, 'l'),
    'latitude': helpers.RecordField(176, 14, 'l'),
    'longitude': helpers.RecordField(201, 14, 'l'),
}

ARB_FIELDS = {
    'record_id': helpers.RecordField(1, 12, 'l'),
    'center_name': helpers.RecordField(13, 40, 'l'),
    'structure': helpers.RecordField(53, 10, 'l'),
    'latitude': helpers.RecordField(63, 14, 'l'),
    'longitude': helpers.RecordField(77, 14, 'l'),
    'description': helpers.RecordField(91, 300, 'l'),
    'seq_num': helpers.RecordField(391, 6, 'l'),
    'nas': helpers.RecordField(397, 1, 'l'),
}

@shared_task
def update_centers():
    effective = helpers.get_latest_date()
    logger.info("Updating ARTCC information to %s NASR cycle...", effective)

    data = {}

    # Process facility file
    aff_fn = helpers.download_latest_file('AFF.zip')
    with ZipFile(aff_fn, 'r') as zf:
        with zf.open('AFF.txt') as aff_file:
            for line in aff_file:
                line_type = helpers.get_field(line, AFF_FIELDS['record_type'])
                if line_type == 'AFF1':
                    facility_type = helpers.get_field(line, AFF_FIELDS['facility_type'])
                    if facility_type == 'ARTCC':
                        facility_id = helpers.get_field(line, AFF_FIELDS['facility_id'])
                        facility_name = helpers.get_field(line, AFF_FIELDS['name'])
                        location = helpers.get_field(line, AFF_FIELDS['location'])
                        state = helpers.get_field(line, AFF_FIELDS['state_code'])
                        lat = helpers.parse_dms(helpers.get_field(line, AFF_FIELDS['latitude']))
                        lon = helpers.parse_dms(helpers.get_field(line, AFF_FIELDS['longitude']))

                        data[facility_id] = {
                            'name': facility_name,
                            'city': location,
                            'state': state,
                            'location': Point(lon, lat),
                            'effective': effective,
                        }

    remove(aff_fn)

    # Process boundary file
    arb_fn = helpers.download_latest_file('ARB.zip')
    cur_facility = ''
    cur_alt = ''
    cur_points = []
    poly = None
    with ZipFile(arb_fn, 'r') as zf:
        with zf.open('ARB.txt') as arb_file:
            for line in arb_file:
                rec_id = helpers.get_field(line, ARB_FIELDS['record_id'])
                facility_id = rec_id.split(' ')[0]
                rec_alt = helpers.get_field(line, ARB_FIELDS['structure'])
                if cur_facility != facility_id or cur_alt != rec_alt:
                    if cur_facility != '':
                        if cur_alt == 'HIGH':
                            cur_points.append(cur_points[0])
                            poly = Polygon(cur_points).buffer(0)
                            if isinstance(poly, Polygon):
                                poly = MultiPolygon(poly)
                            data[cur_facility]['boundary'] = poly
                    cur_facility = facility_id
                    cur_alt = rec_alt
                    cur_points = []
                lat = helpers.parse_dms(helpers.get_field(line, ARB_FIELDS['latitude']))
                lon = helpers.parse_dms(helpers.get_field(line, ARB_FIELDS['longitude']))
                if lon <= -180:
                    lon += 360.0
                cur_points.append((lon, lat))
    remove(arb_fn)

    count = 0
    for facility_id in data:
        rec = data[facility_id]
        if 'boundary' in rec:
            count += 1
            result = Center.objects.update_or_create(code=facility_id, defaults=rec)
            if result[1]:
                logger.info("Created %s-%s...", facility_id, rec['name'])
            else:
                logger.info("Updated %s-%s...", facility_id, rec['name'])

    return count
