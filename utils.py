import pandas as pd

from collections import deque
from typing import Deque, Dict, List

RANGE_PROPERTY_PATHS: List[Deque] = [deque(['props', 'figure', 'layout', 'xaxis', 'range']),
                                     deque(['props', 'figure', 'layout', 'xaxis', 'autorange']),
                                     deque(['props', 'id'])]


def contains_nested_property(entity: Dict, property_path: Deque) -> bool:
    if not len(property_path):
        return True
    next_property = property_path.popleft()
    if entity.get(next_property, None):
        return contains_nested_property(entity[next_property], property_path)
    return False


def range_can_be_altered(entity: Dict) -> bool:
    for property_path in RANGE_PROPERTY_PATHS:
        if not contains_nested_property(entity, property_path):
            return False
    return True


def get_dash_time_format_from_unix_timestamp(unix_time_stamp: int) -> str:
    return pd.Timestamp(unix_time_stamp, unit='s').strftime('%Y-%m-%d')
