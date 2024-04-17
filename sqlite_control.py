import csv
import os
import sqlite3
from typing import Optional

from geojson_utils import convert_to_geojson
from models import GeoJSONFeatureCollection, RouteModel


class SQLiteControl:
    db_file_path: str = "database/sea_routes.db"

    def table_exists(self, table_name):
        db_connection = sqlite3.connect(self.db_file_path)
        db_cursor = db_connection.cursor()
        db_cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            (table_name,),
        )
        result = db_cursor.fetchone()
        db_cursor.close()
        db_connection.close()
        return result is not None

    def insert_data(self, data_file: str) -> None:
        if not os.path.exists(os.path.dirname(self.db_file_path)):
            os.makedirs(os.path.dirname(self.db_file_path))

        db_connection = sqlite3.connect(self.db_file_path)
        db_cursor = db_connection.cursor()
        if self.table_exists("routes"):
            print("Database exists, skipping inseting data")
            return

        db_cursor.execute(
            """CREATE TABLE IF NOT EXISTS routes (route_id TEXT, from_port TEXT, to_port TEXT, leg_duration TEXT, points TEXT)"""
        )

        csv.field_size_limit(1073741824)  # 1GB limit
        with open(data_file, newline="") as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            data_to_insert = [tuple(row) for row in reader]
            db_cursor.executemany(
                """INSERT INTO routes (route_id, from_port, to_port, leg_duration, points) VALUES (?, ?, ?, ?, ?)""",
                data_to_insert,
            )

        db_connection.commit()
        db_cursor.close()
        db_connection.close()

    def get_all_routes(self) -> list[RouteModel]:
        db_connection = sqlite3.connect(self.db_file_path)
        db_cursor = db_connection.cursor()
        returnList = []

        db_cursor.execute(
            "SELECT route_id, from_port, to_port, leg_duration FROM routes"
        )
        rows = db_cursor.fetchall()
        for row in rows:
            route_model = RouteModel(
                route_id=row[0], from_port=row[1], to_port=row[2], leg_duration=row[3]
            )
            returnList.append(route_model)

        db_cursor.close()
        db_connection.close()
        return returnList

    def get_route(self, route_id) -> Optional[GeoJSONFeatureCollection]:
        db_connection = sqlite3.connect(self.db_file_path)
        db_cursor = db_connection.cursor()

        db_cursor.execute(
            "SELECT route_id, from_port, to_port, leg_duration, points FROM routes WHERE route_id = ?",
            (route_id,),
        )
        row = db_cursor.fetchone()
        if row is None:
            return None

        rowDict = {}
        rowDict["route_id"] = row[0]
        rowDict["from_port"] = row[1]
        rowDict["to_port"] = row[2]
        rowDict["leg_duration"] = row[3]
        rowDict["points"] = row[4]

        db_cursor.close()
        db_connection.close()
        return convert_to_geojson(rowDict)
