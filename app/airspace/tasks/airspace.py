from celery import shared_task
from celery.utils.log import get_task_logger
from airspace.tasks import helpers
from zipfile import ZipFile
from shapefile import Reader
from os import remove
from django.contrib.gis.geos import Polygon, MultiPolygon
from airspace.models import Airspace, AirspaceVolume

logger = get_task_logger(__name__)

AIRSPACE_FILES = {
    'Shape_Files/class_b': 'B',
    'Shape_Files/class_c': 'C',
    'Shape_Files/class_d': 'D'
}

@shared_task
def update_airspace():
    effective = helpers.get_latest_date()
    logger.info("Updating airspace information to %s NASR cycle...", effective)

    as_fn = helpers.download_latest_file('class_airspace_shape_files.zip')
    with ZipFile(as_fn, 'r') as zf:
        for filename, classification in AIRSPACE_FILES.items():
            # Extract component files and create shapefile reader
            # Need to extract because ZipFile objects do not support seek
            shp_fn = zf.extract(filename + '.shp', helpers.TEMP_DIR)
            shx_fn = zf.extract(filename + '.shx', helpers.TEMP_DIR)
            dbf_fn = zf.extract(filename + '.dbf', helpers.TEMP_DIR)
            sf = Reader(shp_fn)

            # Iterate over records
            airspaces = {}
            for sr in sf.shapeRecords():
                airspace = sr.record[0]
                name = sr.record[1]
                try:
                    low = float(sr.record[2]) * 0.3048
                except ValueError:
                    low = 0
                high = float(sr.record[3]) * 0.3048
                parts = sr.shape.parts
                parts.append(len(sr.shape.points))
                polys = []
                for i in range(len(parts) - 1):
                    polys.append(Polygon(tuple(tuple(p) for p in sr.shape.points[parts[i]:parts[i+1]])))

                if airspace in airspaces:
                    airspace_obj = airspaces[airspace]
                else:
                    airspace_obj, airspace_created = Airspace.objects.update_or_create(name=airspace, defaults={
                        'name': airspace,
                        'effective': effective,
                        'classification': classification,
                    })
                    airspaces[airspace] = airspace_obj
                    if airspace_created:
                        logger.info("Created airspace %s", airspace)
                    else:
                        logger.info("Updated airspace %s", airspace)
                        AirspaceVolume.objects.filter(parent=airspace_obj).delete()

                for poly in polys:
                    AirspaceVolume.objects.create(
                        name=name,
                        effective=effective,
                        parent=airspace_obj,
                        low_altitude=low,
                        high_altitude=high,
                        boundary=poly
                    )

            # Dispose of temporary resources
            del sf
            remove(shp_fn)
            remove(shx_fn)
            remove(dbf_fn)

    remove(as_fn)
