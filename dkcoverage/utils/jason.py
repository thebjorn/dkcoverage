# -*- coding: utf-8 -*-

"""Helper module to send json encoded data from Python.
"""

# pylint:disable=E0202

import decimal
import datetime
import json
import time
from pathlib import Path


class DkJSONEncoder(json.JSONEncoder):
    "Handle special cases, like Decimal..."

    def default(self, obj):  # pylint:disable=R0911
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        if hasattr(obj, '__json__'):
            return obj.__json__()
        if isinstance(obj, set):
            return list(obj)

        if isinstance(obj, datetime.datetime):
            if obj == datetime.datetime(1899, 12, 30, 0, 0):
                # tsql invalid date
                return None
            return dict(year=obj.year,
                        month=obj.month,
                        day=obj.day,
                        hour=obj.hour,
                        minute=obj.minute,
                        second=obj.second,
                        # new Date(val.jsdate)
                        jsdate=time.mktime(obj.timetuple()) * 1000,
                        kind='DATETIME')
        if isinstance(obj, datetime.date):
            return dict(year=obj.year,
                        month=obj.month,
                        day=obj.day,
                        kind='DATE')
        if isinstance(obj, datetime.time):
            return dict(hour=obj.hour,
                        minute=obj.minute,
                        second=obj.second,
                        microsecond=obj.microsecond,
                        kind="TIME")

        if isinstance(obj, Path):
            return '/'.join(obj.parts)

        if hasattr(obj, '__dict__'):
            return obj.__dict__
        # if isinstance(obj, Path):
        #     import pdb;pdb.set_trace()
        # return obj.__dict__

        return json.JSONEncoder.default(self, obj)


def dumps(val, indent=4, cls=DkJSONEncoder):
    "Dump json value, using our special encoder class."
    return json.dumps(val, sort_keys=True, indent=indent, cls=cls)


def loads(val):
    "For symmetry with dumps."
    return json.loads(val)

