from geopy.exc import GeopyError  # type: ignore
from geopy.geocoders import Nominatim  # type: ignore

from astro_engine.models import GeoLocation

geolocator = Nominatim(user_agent="data_virgo")


def get_place_coordinates(location: str) -> GeoLocation:
    location = location.strip()

    if not location:
        raise ValueError("Location cannot be empty string")

    try:
        place = geolocator.geocode(location)  # type: ignore

        if place is None:
            raise ValueError(f'"{location}" - no such place found')
    except GeopyError as e:
        raise RuntimeError(f'Geocode failed for location "{location}": {e}') from e

    return GeoLocation(
        place_name=location, latitude=place.latitude, longitude=place.longitude  # type: ignore
    )
