import csv
from typing import Optional
from sqlalchemy import create_engine, select
from sqlalchemy import Table, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlmodel import col
from geojson_utils import convert_to_geojson
from models import GeoJSONFeatureCollection, RouteModel

Base = declarative_base()

class Route(Base): # type: ignore
    __tablename__ = 'routes'
    route_id = Column(Integer, primary_key=True)
    from_port = Column('from_port', String)
    to_port = Column('to_port', String)
    leg_duration = Column('leg_duration', Float)
    points = Column('points', String)
    
    
class PostgreSQLControl:
    POSTGRES_ADDRESS = 'localhost'
    POSTGRES_PORT = '5432'
    POSTGRES_USERNAME = 'postgres'
    POSTGRES_PASSWORD = 'database'
    POSTGRES_DBNAME = 'PythonChallenge'
    postgres_str = f'postgresql://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_ADDRESS}:{POSTGRES_PORT}/{POSTGRES_DBNAME}'
    routes_table : Table
    
    def __init__(self):
        self.engine = create_engine(self.postgres_str)
        Base.metadata.create_all(self.engine)
        self.routes_table = Base.metadata.tables['routes']

    def insert_data(self, data_file: str) -> None:
        Session = sessionmaker(bind=self.engine)
        session = Session()

        csv.field_size_limit(1073741824)  # 1GB limit
        with open(data_file, newline="") as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip header
            data_to_insert = [self.create_route(row) for row in reader]
            session.add_all(data_to_insert)

        try:
            session.commit()
        except Exception:
            print("Data insertion skipped...")
        session.close()
        
    def create_route(self, variables : list[str]) -> Route:
        return Route(
            route_id=int(variables[0]),
            from_port=variables[1],
            to_port=variables[2],
            leg_duration=float(variables[3]),
            points=variables[4]
        )

    def get_all_routes(self) -> list[RouteModel]:
        with self.engine.connect() as connection:
            query = select(self.routes_table.c["route_id", "from_port", "to_port", "leg_duration"]) # type: ignore
            result = connection.execute(query)
            rows = result.fetchall()
            
        returnList = []
        for row in rows:
            route_model = RouteModel(
                route_id=row[0], from_port=row[1], to_port=row[2], leg_duration=row[3]
            )
            returnList.append(route_model)
            
        return returnList

    def get_route(self, route_id) -> Optional[GeoJSONFeatureCollection]:
        with self.engine.connect() as connection:
            query = select(self.routes_table.c["route_id", "from_port", "to_port", "leg_duration", "points"]).where(self.routes_table.c.route_id == route_id) # type: ignore
            result = connection.execute(query)
            row = result.fetchone()
            
        if row is None:
            return None

        rowDict = {}
        rowDict["route_id"] = row[0]
        rowDict["from_port"] = row[1]
        rowDict["to_port"] = row[2]
        rowDict["leg_duration"] = row[3]
        rowDict["points"] = row[4]
        
        return convert_to_geojson(rowDict)
