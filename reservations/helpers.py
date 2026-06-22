from django.utils import timezone
from datetime import datetime

def get_reservation_type(checkin, checkout):
    """ Returns whether the reservation is daily (1), weekly (2), or monthly (3) """
    checkin_dt = datetime.fromisoformat(checkin).replace(tzinfo=timezone.UTC)
    checkout_dt = datetime.fromisoformat(checkout).replace(tzinfo=timezone.UTC)
    delta = checkout_dt - checkin_dt
    months = delta.days / 30
    weeks = delta.days / 7
    if months >= 1:
        return 3
    elif weeks >= 1:
        return 2
    return 1

DATE_FORMATS = [
    '%m/%d/%Y %I:%M %p',        # 06/22/2026 02:30 PM (desktop flatpickr)
    '%m/%d/%Y at %I:%M %p',     # 06/22/2026 at 02:30 PM (mobile flatpickr)
    '%m/%d/%Y %H:%M',           # 06/22/2026 14:30 (24hr variation)
    '%Y-%m-%d %H:%M',           # 2026-06-22 14:30 (ISO-ish)
    '%Y-%m-%dT%H:%M',           # 2026-06-22T14:30 (ISO with T)
    '%m/%d/%Y %I:%M%p',         # 06/22/2026 02:30PM (no space before AM/PM)
    '%m/%d/%Y, %I:%M %p',       # 06/22/2026, 02:30 PM (comma variation)
    '%m/%d/%Y at %H:%M',        # 06/22/2026 at 14:30 (mobile 24hr)
]

def parse_datetime(date_str):
    if not date_str:
        raise ValueError("Empty date string")
    date_str = ' '.join(date_str.split())
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    raise ValueError(f"Unable to parse date string: {repr(date_str)}")
