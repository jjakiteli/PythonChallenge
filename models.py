from typing import Any, List

from pydantic import BaseModel
from pydantic_geojson import FeatureModel


class RouteModel(BaseModel):
    route_id: int
    from_port: str
    to_port: str
    leg_duration: int


class GeoJSONFeature(FeatureModel):
    properties: dict[str, Any]


class GeoJSONFeatureCollection(BaseModel):
    type: str = "FeatureCollection"
    features: List[GeoJSONFeature]
