import os
import time
import csv
from collections import defaultdict, deque
import datetime

from ..base import BaseDataClient
from .config import CSV_FIELDS, CSV_FILE_FORMAT, TIMESTAMP_INDEX

from cryptocore.utils.time_utils import (
    GET_YEAR_DAY_HOUR, get_timetuple, get_tuples_in_interval, ensure_start_end, get_timetuple_since
)
from cryptocore.contracts.base import BaseContract

class QuoteTimed(BaseContract):
    def __init__(self, time_func):
        self.time_func = time_func

    def validate(self, value):
        if "timestamp" not in value:
            return False

        return (
            get_timetuple(value["timestamp"]) == self.time_func()
            and super().validate(value)
        )

class CSVHistoricalDataClient(BaseDataClient):
    """
    Data Directory Structure
    data/
        year_day(365)/
            hour(24)/
                <ticker>_year_day_hour.csv
                    :fields - QuoteContract fields
    """

    def __init__(self, exchange):
        BaseDataClient.__init__(self, exchange)
        self.tickers_list = set()
        self.csv_writers = {}
        self.writer_timetuple = get_timetuple(time.time())
        self.quote_time_validator = QuoteTimed(self.get_writer_timetuple)
        self.loaded_data = defaultdict(list)


    @staticmethod
    def get_csv_file_path(ticker, time_tuple):
        return CSV_FILE_FORMAT.format(ticker, *time_tuple)


    def get_writer_timetuple(self):
        return self.writer_timetuple


    def get_latest_quote_data(self, tickers, previous_n=1):
        returned_data = defaultdict(list)

        for ticker in tickers:
            returned_data[ticker] = returned_data[ticker][:-previous_n]

        return returned_data


    def get_between_quote_data(self, tickers, start=None, end=None):
        start, end = ensure_start_end(start, end)
        returned_data = defaultdict(list)

        for ticker in tickers:
            list_data = returned_data[ticker]
            for quote in self.loaded_data[ticker]:
                timestamp = quote["timestamp"]
                if timestamp < start:
                    continue
                if timestamp > end:
                    break
                list_data.append(quote)

        return returned_data


    def load_latest_quote_data(self, tickers, previous_n=1):
        current_timetuple = get_timetuple(time.time())
        for ticker in tickers:
            data = deque(maxlen=previous_n)

            while len(deque) < previous_n:
                csv_path = CSV_FILE_FORMAT(ticker, current_timetuple)
                with open(csv_path, "r", encoding="utf-8") as f:
                    reader = csv.reader(f)
                    next(reader) # skip header
                    for line in reader:
                        data.append(line)
                current_timetuple = get_timetuple_since(current_timetuple, hour=-1)

            self.loaded_data[ticker] = list(data)


    def load_between_quote_data(self, tickers, start=None, end=None):
        start, end = ensure_start_end(start, end)

        for ticker in tickers:
            data = []
            for timetuple in get_tuples_in_interval(start, end):
                csv_path = CSV_FILE_FORMAT(ticker, timetuple)

                with open(csv_path, "r", encoding="utf-8") as f:
                    reader = csv.reader(f)
                    next(reader)  # skip header
                    for line in reader:
                        timestamp = float(line[TIMESTAMP_INDEX])
                        if timestamp < start:
                            continue
                        if timestamp > end:
                            break
                        data.append(line)

            self.loaded_data[ticker] = data


    def list_tickers(self):
        return sorted(self.tickers_list)


    def save_quotes_data(self, quote_infos):
        super().save_quotes_data(quote_infos)

        for quote_info in quote_infos:
            ticker = quote_info["ticker"]
            self.get_csv_writer(ticker).writerows([quote_info[field] for field in CSV_FIELDS])

        self._sync_csv_writers()


    def get_csv_writer(self, ticker):
        self.csv_writers[ticker] = _, csv_writer = self.csv_writers.get(ticker, self._create_csv_writer(
            ticker,
            CSVHistoricalDataClient.get_writer_timetuple
        ))

        return csv_writer


    def _validate_quote(self, quote_info):
        return self.quote_time_validator.validate(quote_info) and super()._validate_quote(quote_info)


    @classmethod
    def _create_csv_writer(cls, ticker, time_tuple):
        """
        Returns time_tuple and ticker-associated csv_writer
        """
        path = CSVHistoricalDataClient.get_csv_file_path(ticker, time_tuple)

        if not os.path.exists(path):
            f = open(path, "a", encoding="utf-8")
            f.write(",".join(CSV_FIELDS))
        else:
            f = open(path, "a", encoding="utf-8")

        csv_writer = csv.writer(f, delimiter=",")
        return time_tuple, csv_writer


    def _sync_csv_writers(self):
        self.writer_timetuple = get_timetuple(time.time())

        for ticker in self.tickers_list:
            time_tuple, csv_writer = self.csv_writers.get(ticker)

            if csv_writer is None or time_tuple != self.writer_timetuple:
                self.csv_writers[ticker] = self._create_csv_writer(
                    ticker,
                    self.get_writer_timetuple()
                )
