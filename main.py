from fastapi import FastAPI

from dependencies import SQLiteRepository
from geojson_utils import convert_to_geojson


app = FastAPI()

@app.get("/routes")
async def get_routes(sqlite_control: SQLiteRepository):
    return sqlite_control.get_all_routes()


@app.get("/routes/{route_id}")
async def get_routes(route_id: int, sqlite_control: SQLiteRepository):
    return convert_to_geojson(sqlite_control.get_route(route_id))

