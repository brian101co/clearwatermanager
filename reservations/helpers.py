import pytz

from datetime import datetime

def get_reservation_type(checkin, checkout):
    """ Returns whether the reservation is daily (1), weekly (2), or monthly (3) """
    checkin_dt = datetime.fromisoformat(checkin).replace(tzinfo=pytz.UTC)
    checkout_dt = datetime.fromisoformat(checkout).replace(tzinfo=pytz.UTC)
    delta = checkout_dt - checkin_dt
    months = delta.days / 30
    weeks = delta.days / 7
    if months >= 1:
        return 3
    elif weeks >= 1:
        return 2
    return 1
