## GPS Math

from dataclasses import dataclass
from statistics import mean
from math import cos, pi, sqrt
from typing import List, Union

EARTH_CIRCUMF = 40074000

@dataclass
class LatLong:
    lat: float
    long: float
    label: Union[str, None] = None

LatLongs = List[LatLong]

@dataclass
class Point:
    x: float
    y: float

def get_mean_latlong(coords: LatLongs):
    lats = [coord.lat for coord in coords]
    longs = [coord.long for coord in coords]

    return LatLong(
            lat = mean(lats),
            long = mean(longs)
            )

def LatLongToPoint(coord: LatLong, ref: LatLong):
  return Point(
          x = (coord.lat - ref.lat) / 360 * EARTH_CIRCUMF,
          y = (coord.long - ref.long) / 360 * cos(ref.lat*pi/180) * EARTH_CIRCUMF,
          )

def PointToLatLong(coord: Point, ref: LatLong):
    return LatLong(
            lat = (coord.y * 360 / EARTH_CIRCUMF) + ref.lat,
            long = (coord.x * 360 / EARTH_CIRCUMF / cos(ref.lat*pi/180)) + ref.long
            )

def PointDistance(point1: Point, point2: Point):
    dx = point1.x - point2.x
    dy = point2.y - point1.y

    dst = sqrt(dx*dx + dy*dy)

    return dst


def get_latlong_stats(coords: LatLongs):
    ref = get_mean_latlong(coords)

    indexed_coords = list(zip(range(len(coords)), coords))

    coord_pairs = []
    for coord in indexed_coords:
        for coord2 in indexed_coords:
            if coord[0] < coord2[0]:
                coord_pairs.append((coord[1], coord2[1]))

    coord_dx = []

    for coord_pair in coord_pairs:
        dx = PointDistance(LatLongToPoint(coord_pair[0], ref),LatLongToPoint(coord_pair[1], ref))
        coord_dx.append((dx))

    from pprint import pprint
    pprint(locals())

