from domain.gps import Gps
from dataclasses import dataclass


@dataclass
class Parking:
    empty_count: int
    longitude: float
    latitude: float