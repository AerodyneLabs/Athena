from celery import shared_task
from celery.utils.log import get_task_logger
from airspace.tasks import helpers
from airspace.models import Center, Tower
from zipfile import ZipFile
from django.contrib.gis.geos import Point
from os import remove

logger = get_task_logger(__name__)

TWR_FIELDS = {
    'record_type': helpers.RecordField(1, 4, 'l'),
    'facility_id': helpers.RecordField(5, 4, 'l'),
    'site_number': helpers.RecordField(19, 11, 'l'),
    'region': helpers.RecordField(30, 3, 'l'),
    'state': helpers.RecordField(63, 2, 'l'),
    'city': helpers.RecordField(65, 40, 'l'),
    'name': helpers.RecordField(105, 50, 'l'),
    'latitude': helpers.RecordField(155, 14, 'l'),
    'longitude': helpers.RecordField(180, 14, 'l'),
    'fss_id': helpers.RecordField(205, 4, 'l'),
    'fss_name': helpers.RecordField(209, 30, 'l'),
    'facility_type': helpers.RecordField(239, 12, 'l'),
    'operation_hours': helpers.RecordField(251, 2, 'l'),
    'operation_regularity': helpers.RecordField(253, 3, 'l'),
    'master_id': helpers.RecordField(256, 4, 'l'),
    'master_name': helpers.RecordField(260, 50, 'l'),
}

@shared_task
def update_towers():
    effective = helpers.get_latest_date()
    logger.info("Updating tower information to %s NASR cycle...", effective)

    defferred = []

    twr_fn = helpers.download_latest_file('TWR.zip')
    with ZipFile(twr_fn, 'r') as zf:
        with zf.open('TWR.txt') as twr_file:
            for line in twr_file:
                line_type = helpers.get_field(line, TWR_FIELDS['record_type'])
                if line_type == 'TWR1':
                    facility_type = helpers.get_field(line, TWR_FIELDS['facility_type'])
                    facility_id = helpers.get_field(line, TWR_FIELDS['facility_id'])
                    region = helpers.get_field(line, TWR_FIELDS['region'])
                    state = helpers.get_field(line, TWR_FIELDS['state'])
                    city = helpers.get_field(line, TWR_FIELDS['city'])
                    name = helpers.get_field(line, TWR_FIELDS['name'])
                    master_id = helpers.get_field(line, TWR_FIELDS['master_id'])
                    lat = helpers.parse_dms(helpers.get_field(line, TWR_FIELDS['latitude']))
                    lon = helpers.parse_dms(helpers.get_field(line, TWR_FIELDS['longitude']))

                    center = None
                    # logger.debug("Finding center with id: %s", region)
                    # center = Center.objects.get(code=region).id
                    # logger.debug("Found center with pk: %s", center)

                    data = {
                        'code': facility_id,
                        'name': name,
                        'station_type': facility_type,
                        'effective': effective,
                        'artcc': center,
                        'location': Point(lon, lat),
                        'city': city,
                        'state': state,
                        'master': None,
                    }

                    if master_id is not '':
                        data['master'] = master_id
                        defferred.append(data)
                        continue

                    result = Tower.objects.update_or_create(code=facility_id, defaults=data)
                    if result[1]:
                        logger.info("Created %s-%s...", facility_id, data['name'])
                    else:
                        logger.info("Updated %s-%s...", facility_id, data['name'])
    remove(twr_fn)

    for record in defferred:
        facility_id = record['code']
        master = Tower.objects.get(code=record['master'])
        record['master'] = master
        result = Tower.objects.update_or_create(code=facility_id, defaults=record)
        if result[1]:
            logger.info("Created %s-%s...", facility_id, data['name'])
        else:
            logger.info("Updated %s-%s...", facility_id, data['name'])
