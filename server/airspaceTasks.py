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


def get_latest_url():
    prefix = 'https://nfdc.faa.gov/webContent/56DaySub/'
    folder = '{0}/'.format(get_latest_date())
    return prefix + folder + 'NAV.zip'


def download_latest_nav():
    # Get file url
    url = get_latest_url()
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
