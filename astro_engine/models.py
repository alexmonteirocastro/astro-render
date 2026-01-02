from enum import Enum
from typing import Dict, List, Literal, Optional

from pydantic import BaseModel

# ---------- Meta ----------


class GeoCoordinates(BaseModel):
    lat: float
    lon: float


class GeoLocation(BaseModel):
    latitude: float
    longitude: float
    place_name: str


class HouseSystem(Enum):
    PLACIDUS = "P"
    REGIOMONTANUS = "R"
    EQUAL_HOUSES = "E"
    WHOLE_SIGN = "W"
    TOPOCENTRIC = "T"
    MORINUS = "M"


class TZInfo(BaseModel):
    mode: Literal["tzid", "offset", "local"] | str  # allow future modes
    tzid: Optional[str] = None
    offset: Optional[str] = None


class MetaData(BaseModel):
    local: str
    ut: str
    jd_ut: float
    geo: GeoCoordinates
    hsys: HouseSystem
    tz: TZInfo


# ---------- Planets ----------
Motion = Literal["DIRECT", "RETRO", "STATION"] | str


class DMS(BaseModel):
    deg: int
    min: int
    sec: float


class Body(BaseModel):
    sign: str
    pos: DMS
    lon: float


class PlanetaryBody(Body):
    lat: float
    dist_au: float
    speed_lon_deg_per_day: float
    motion: Motion
    house: int


class Planets(BaseModel):
    station_threshold_speed_lon_deg_per_day: float
    bodies: Dict[str, PlanetaryBody]


# ---------- Houses ----------


class Houses(BaseModel):
    asc: Body
    mc: Body
    cusps: Dict[str, Body]


# ---------- Aspects ----------


class AspectDefinition(BaseModel):
    name: str
    symbol: str
    angle: int


AspectPhase = Literal["APPLY", "SEPAR"] | str


class Aspect(BaseModel):
    body1: str
    body2: str
    aspect: AspectDefinition
    orb: float
    phase: AspectPhase


# ---------- Results ----------


class AstrologicalData(BaseModel):
    meta: MetaData
    planets: Planets
    houses: Houses
    aspects: List[Aspect]
