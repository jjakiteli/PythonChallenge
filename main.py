from fastapi import FastAPI, HTTPException

from dependencies import SQLiteRepository, get_sqlite_control
from models import GeoJSONFeatureCollection, RouteModel

# Create db if doesnt exist
get_sqlite_control().insert_data("web_challenge.csv")
# Start App
app = FastAPI()


@app.get("/routes")
async def get_all_routes(sqlite_control: SQLiteRepository) -> list[RouteModel]:
    return sqlite_control.get_all_routes()


@app.get("/routes/{route_id}")
async def get_route(
    route_id: int, sqlite_control: SQLiteRepository
) -> GeoJSONFeatureCollection | None:
    geojson = sqlite_control.get_route(route_id)
    if geojson is None:
        raise HTTPException(status_code=404, detail="No route found")
    return sqlite_control.get_route(route_id)
