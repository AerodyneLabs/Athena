from collections import namedtuple
from datetime import date
from math import floor
from requests import get

TEMP_DIR = 'data/'

RecordField = namedtuple('RecordField', ['start', 'length', 'just'])

def get_field(record, field):
    """Return the contents of a field from the record as a string."""
    # Extract field based on start position and length
    value = record[field.start-1:field.start+field.length-1]
    # Strip white space based on justification
    if field.just == 'l':
        return value.rstrip()
    elif field.just == 'r':
        return value.lstrip()
    else:
        return value

def parse_dms(x):
    """Return a float representation of a dd-mm-ss.ssH string."""
    # Split the string into tokens
    tokens = x.split('-')
    # Convert tokens to floats
    try:
        degrees = float(tokens[0])
        minutes = float(tokens[1])
        seconds = float(tokens[2][:-1])
    except ValueError:
        return False
    # Parse hemisphere value
    dec = 1.0
    if tokens[2][-1] in ['S', 'W']:
        dec = -1.0
    return (degrees + (minutes / 60.0) + (seconds / 3600.0)) * dec

def parse_variation(x):
    """Return a flaot representation of a ddH string."""
    # Convert degrees to float
    degrees = float(x[:-1])
    if x[-1] == 'E':
        return degrees
    else:
        return -degrees

def parse_boolean(x):
    """Return a boolean representation of a y/n string."""
    if x in ['y', 'Y']:
        return True
    else:
        return False

def get_latest_date():
    """Return the latest date on the 56 day update cycle."""
    ref_ord = date(2015, 1, 8).toordinal()
    cur_ord = date.today().toordinal()
    seq = int(floor((cur_ord - ref_ord) / 56))
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
