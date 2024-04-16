import geojson
import json


def convert_to_geojson(data: dict) -> dict:
    data_points = json.loads(data["points"])
    
    features = []
    for point in data_points:
        lon, lat, timestamp, value = point
        point_feature = geojson.Point((lon, lat))
        feature_properties = {"timestamp": timestamp, "value": value}
        feature = geojson.Feature(geometry=point_feature, properties=feature_properties)
        features.append(feature)
        
    feature_collection = geojson.FeatureCollection(features)
    
    return feature_collection