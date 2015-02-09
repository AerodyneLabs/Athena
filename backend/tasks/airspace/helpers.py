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
        return value.strip()
    else:
        return value


def parse_dms(x):
    """Return a float representation of a dd-mm-ss.ssH string."""
    # Split the string into tokens
    tokens = x.split('-')
    # Convert string tokens to floats
    try:
        deg = float(tokens[0])
        min = float(tokens[1])
        sec = float(tokens[2][:-1])
    except ValueError:
        return False
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
    # FIXME status updating
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
