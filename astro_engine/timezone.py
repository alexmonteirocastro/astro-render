from timezonefinder import timezone_at


def get_IANA_tz(latitude: float, longitude: float) -> str:
    tz_id = timezone_at(lat=latitude, lng=longitude)

    if tz_id is None:
        raise ValueError("No timezone ID found")

    return tz_id
