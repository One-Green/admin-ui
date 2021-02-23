import pytz
import datetime


def apply_timezone_datetime(_local_tz: str, _time: datetime.time):
    """
    set time zone + merge now().date() with time()
    :param _local_tz:
    :param _time:
    :return:
    """
    return pytz.timezone(_local_tz).localize(
        datetime.datetime.combine(
            datetime.datetime.now().date(),
            _time
        )
    )
