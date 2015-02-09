from helpers import download_latest_file
from worker import app
from tasks.mongoTask import MongoTask
from os.path import dirname
from zipfile import ZipFile
from shapefile import Reader
import geojson
from os import remove


airspace_files = {
    'Shape_Files/class_b': 'Class B',
    'Shape_Files/class_c': 'Class C',
    'Shape_Files/class_d': 'Class D'
}


@app.task(base=MongoTask, bind=True)
def update_airspaces(self):
    # Download latest file
    filename = download_latest_file('class_airspace_shape_files.zip')
    # Construct temp dir
    temp_dir = dirname(filename)
    # Open input zip file
    zf = ZipFile(filename)
    # Open the database
    store = update_airspaces.mongo.airspace.airspaces
    store.remove()
    # Iterate different airspace types
    count = 0
    for airspace_name, airspace_class in airspace_files.iteritems():
        # Extract component files
        shp_fn = zf.extract(airspace_name + '.shp', temp_dir)
        shx_fn = zf.extract(airspace_name + '.shx', temp_dir)
        dbf_fn = zf.extract(airspace_name + '.dbf', temp_dir)
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
            bounds = geojson.Polygon([[
                (bbox[0], bbox[1]),
                (bbox[2], bbox[1]),
                (bbox[2], bbox[3]),
                (bbox[0], bbox[3]),
                (bbox[0], bbox[1])
            ]])
            feature = geojson.Feature(
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
