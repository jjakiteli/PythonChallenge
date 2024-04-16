from pydantic import BaseModel
from typing import List

class RouteModel(BaseModel):
    route_id: int
    from_port: str
    to_port: str
    leg_duration: int
    
class GeoJSONFeature(BaseModel):
    type: str = "Feature"
    geometry: dict
    properties: dict
    
class GeoJSONFeatureCollection(BaseModel):
    type: str = "FeatureCollection"
    features: List[GeoJSONFeature]