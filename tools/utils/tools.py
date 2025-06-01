import datetime

def get_current_utc_timestamp() -> str:
    """
    Return the current UTC time in the format: YYYY-MM-DDTHH:MM:SS.ffffff0Z
    (i.e., 7 digits of fractional seconds, ending with 'Z').
    """
    now = datetime.datetime.now(datetime.timezone.utc)
    # now.microsecond is 0–999999 (6 digits); append '0' for a 7th digit
    fraction = f"{now.microsecond:06d}0"
    return f"{now.year:04d}-{now.month:02d}-{now.day:02d}T" \
           f"{now.hour:02d}:{now.minute:02d}:{now.second:02d}." \
           f"{fraction}Z"
