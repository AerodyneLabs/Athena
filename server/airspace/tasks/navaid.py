from celery import shared_task
from celery.utils.log import get_task_logger
from airspace.tasks import helpers
from airspace.models.navaid import Navaid
from zipfile import ZipFile
from django.contrib.gis.geos import Point
from os import remove

logger = get_task_logger(__name__)

NAV_FIELDS = {
    'record_type': helpers.RecordField(1, 4, 'l'),
    'facility_id': helpers.RecordField(5, 4, 'l'),
    'facility_type': helpers.RecordField(9, 20, 'l'),
    'name': helpers.RecordField(43, 30, 'l'),
    'city': helpers.RecordField(73, 40, 'l'),
    'state': helpers.RecordField(143, 2, 'l'),
    'country': helpers.RecordField(148, 30, 'l'),
    'common': helpers.RecordField(280, 1, 'l'),
    'public': helpers.RecordField(281, 1, 'l'),
    'class': helpers.RecordField(282, 11, 'l'),
    'latitude': helpers.RecordField(372, 14, 'l'),
    'longitude': helpers.RecordField(397, 14, 'l'),
    'elevation': helpers.RecordField(473, 7, 'r'),
    'variation': helpers.RecordField(480, 5, 'r'),
    'status': helpers.RecordField(767, 30, 'l'),
}

TYPE_FILTER = [
    'VOR',
    'DME',
    'VOR/DME',
    'VORTAC',
    'TACAN',
]

@shared_task
def update_navaids():
    count = 0
    effective = helpers.get_latest_date()
    logger.info("Updating navaid information to %s NASR cycle...", effective)

    nav_fn = helpers.download_latest_file('NAV.zip')
    with ZipFile(nav_fn, 'r') as zf:
        with zf.open('NAV.txt') as nav_file:
            for line in nav_file:
                line_type = helpers.get_field(line, NAV_FIELDS['record_type'])
                if line_type == 'NAV1':
                    facility_type = helpers.get_field(line, NAV_FIELDS['facility_type'])
                    if facility_type in TYPE_FILTER:
                        country = helpers.get_field(line, NAV_FIELDS['country'])
                        if country != "": continue
                        code = helpers.get_field(line, NAV_FIELDS['facility_id'])
                        name = helpers.get_field(line, NAV_FIELDS['name'])
                        city = helpers.get_field(line, NAV_FIELDS['city'])
                        state = helpers.get_field(line, NAV_FIELDS['state'])
                        lat = helpers.parse_dms(helpers.get_field(line, NAV_FIELDS['latitude']))
                        lon = helpers.parse_dms(helpers.get_field(line, NAV_FIELDS['longitude']))
                        elevation = 0.3048 * float(helpers.get_field(line, NAV_FIELDS['elevation']))
                        variation = helpers.parse_variation(helpers.get_field(line, NAV_FIELDS['variation']))
                        facility_class = helpers.get_field(line, NAV_FIELDS['class'])
                        service_volume = facility_class[0]

                        location = Point(lon, lat, elevation)
                        
                        result = Navaid.objects.update_or_create(code=code, defaults={
                            'code': code,
                            'name': name,
                            'effective': effective,
                            'location': location,
                            'city': city,
                            'state': state,
                            'variation': variation,
                            'service_volume': service_volume,
                            'station_type': facility_type,
                        })
                        count += 1
                        if result[1]:
                            logger.info("Created %s-%s", code, name)
                        else:
                            logger.info("Updated %s-%s", code, name)

    return count
