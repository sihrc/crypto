import os

from .historical import CSVHistoricalDataClient
from ..base import QuoteContract
from cryptocore.config import CSV_DATA_DIR

CSV_FILE_FORMAT = os.path.join(
    CSV_DATA_DIR, "{ticker}", "{year}_{day}_{hour}_{ticker}.csv"
)

CSV_FIELDS = QuoteContract.fields
TIMESTAMP_INDEX = CSV_FIELDS.index("timestamp")