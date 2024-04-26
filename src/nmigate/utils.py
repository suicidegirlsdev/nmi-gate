import calendar
from datetime import date, datetime


def card_expiration_as_date(mmyy):
    """Return a date for the last day of the mo/yr (ints)."""
    dt = datetime.strptime(mmyy, "%m%y")
    __, exp_day = calendar.monthrange(dt.month, dt.year)
    return date(dt.year, dt.month, exp_day)
