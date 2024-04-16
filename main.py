from fastapi import FastAPI

from dependencies import SQLiteRepository, get_sqlite_control


get_sqlite_control().insert_data('web_challenge.csv')
app = FastAPI()

@app.get("/routes")
async def get_routes(sqlite_control: SQLiteRepository):
    return sqlite_control.get_all_routes()


@app.get("/routes/{route_id}")
async def get_routes(route_id: int, sqlite_control: SQLiteRepository):
    return sqlite_control.get_route(route_id)

