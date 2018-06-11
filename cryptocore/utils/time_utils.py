import time
import calendar
import datetime
from operator import attrgetter

GET_YEAR_DAY_HOUR = attrgetter("tm_year", "tm_yday", "tm_hour")


def get_timetuple(timestamp):
    return GET_YEAR_DAY_HOUR(
        time.gmtime(timestamp)
    )

def get_tuples_in_interval(start, end):
    """
    start / end are seconds since epoch
    """
    start_year, start_day, start_hour = get_timetuple(start)
    end_year, end_day, end_hour = get_timetuple(end)

    num_days_in_year = 365 if calendar.isleap(start_year) else 366
    while (start_year, start_day, start_hour) != (end_year, end_day, end_hour):
        yield (start_year, start_day, start_hour)

        start_hour += 1
        if start_hour == 24:
            start_hour = 0
            start_day += 1

        if start_day > num_days_in_year:
            if start_year == end_year:
                break
            start_day = 1
            start_year += 1
            num_days_in_year = 365 if calendar.isleap(start_year) else 366


def get_timetuple_since(timetuple, **timedelta):
    dt = datetime.datetime(timetuple[0], 1, 1, hour=timetuple[2])
    dt += datetime.timedelta(day=timetuple[1] - 1)
    dt += datetime.timedelta(timedelta)
    return get_timetuple(dt.timestamp())


def ensure_start_end(start, end):
    start = start or 0
    end = end or time.time()

    assert end > start
    return start, end


if __name__ == "__main__":
    current_time = time.time()
    start_time = current_time - 60 * 60 * 24 * 2
    results = list(get_tuples_in_interval(start_time, current_time))

    assert len(results) == 48
