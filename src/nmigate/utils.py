import calendar
from datetime import date, datetime


def card_expiration_as_date(mmyy):
    """Return a date for the last day of the mo/yr (ints)."""
    dt = datetime.strptime(mmyy, "%m%y")
    __, exp_day = calendar.monthrange(dt.year, dt.month)
    return date(dt.year, dt.month, exp_day)


def normalize_merchant_defined_fields(merchant_defined_fields):
    return {
        f"merchant_defined_field_{k}": v
        for k, v in merchant_defined_fields.items()
        if isinstance(k, int) or not k.startswith("merchant_defined_field_")
    }
