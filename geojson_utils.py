import json

from pydantic_geojson import PointModel

from models import GeoJSONFeature, GeoJSONFeatureCollection


def convert_to_geojson(data: dict) -> GeoJSONFeatureCollection:
    data_points = json.loads(data["points"])

    features = []
    for point in data_points:
        lon, lat, timestamp, value = point
        point_feature = PointModel(coordinates=(lon, lat))
        feature_properties = {"timestamp": timestamp, "value": value}
        feature = GeoJSONFeature(geometry=point_feature, properties=feature_properties)
        features.append(feature)

    feature_collection = GeoJSONFeatureCollection(features=features)
    return feature_collection
