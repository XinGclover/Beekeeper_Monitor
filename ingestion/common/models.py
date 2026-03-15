from dataclasses import dataclass


@dataclass
class Location:
    """Represents a geographic location used for data collection."""
    location_id: int
    latitude: float
    longitude: float