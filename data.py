import gps

from dataclasses import dataclass
from typing import List
from dataclasses_serialization.json import JSONStrSerializer

import numpy as np

@dataclass
class ReceiveRecord:
    receiverCoord: gps.LatLong
    ts: float

@dataclass
class ReceiveRecords:
    records: List[ReceiveRecord]

def load_records(f):
    rcs = JSONStrSerializer.deserialize(ReceiveRecords, f.read())
    return rcs.records

def save_records(records: List[ReceiveRecord], f):
    rcs = ReceiveRecords(records)
    f.write(JSONStrSerializer.serialize(rcs))


