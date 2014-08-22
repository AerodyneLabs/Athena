from datetime import date
from math import floor


def get_latest_date():
    # Find latest date on the 56 day cycle
    ref_ord = date(2014, 5, 29).toordinal()
    cur_ord = date.today().toordinal()
    seq = int(floor((cur_ord - ref_ord) / 56))
    latest = date.fromordinal(seq * 56 + ref_ord)
    return latest
