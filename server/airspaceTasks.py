from datetime import date
from math import floor


def get_url():
    # Find latest date on the 56 day cycle
    ref_ord = date(2014, 5, 29).toordinal()
    cur_ord = date.today().toordinal()
    seq = int(floor((cur_ord - ref_ord) / 56))
    latest = date.fromordinal(seq * 56 + ref_ord)
    # Generate url
    prefix = 'https://nfdc.faa.gov/webContent/56DaySub/'
    filename = 'aixm5.1.zip'
    folder = '{0}/'.format(latest)
    return prefix + folder + filename
