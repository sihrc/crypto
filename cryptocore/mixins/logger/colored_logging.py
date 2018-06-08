#!/usr/bin/env python

from copy import copy
from logging import Formatter

MAPPING = {
    'DEBUG': 37,  # white
    'INFO': 36,  # cyan
    'WARNING': 33,  # yellow
    'ERROR': 31,  # red
    'CRITICAL': 41,  # white on red bg
}

PREFIX = '\033['
SUFFIX = '\033[0m'


def color(color, text):
    return '{0}{1}m{2}{3}'.format(
        PREFIX,
        color,
        text,
        SUFFIX
    )


class ColoredFormatter(Formatter):
    def format(self, record):
        colored_record = copy(record)
        levelname = colored_record.levelname
        seq = MAPPING.get(levelname, 37)  # default white
        colored_record.levelname = color(seq, colored_record.levelname)

        colored_record.request_id = color(
            94, str(colored_record.request_id)[:8])
        colored_record.identity = color(94, colored_record.identity)
        colored_record.location = color(90, "({filename}:{lineno})".format(
            filename=colored_record.filename,
            lineno=colored_record.lineno
        ))
        colored_record.message_header = color(36, "message:")

        return super().format(colored_record)
