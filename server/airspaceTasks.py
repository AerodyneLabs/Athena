from datetime import date
from math import floor
from requests import get


TEMP_DIR = 'data/'


def get_latest_date():
    # Find latest date on the 56 day cycle
    ref_ord = date(2014, 5, 29).toordinal()
    cur_ord = date.today().toordinal()
    seq = int(floor((cur_ord - ref_ord) / 56))
    latest = date.fromordinal(seq * 56 + ref_ord)
    return latest


def download_latest():
    # Get file url
    latest_date = get_latest_date()
    prefix = 'https://nfdc.faa.gov/webContent/56DaySub/'
    filename = 'aixm5.1.zip'
    folder = '{0}/'.format(latest_date)
    url = prefix + folder + filename
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
