import sqlite3
import csv
import os


class SQLiteControl:
    db_file_path: str = 'database/sea_routes.db'
        
    def __init__(self) -> None:
        self.insert_data('web_challenge.csv')
        
    def table_exists(self, table_name):
        db_connection = sqlite3.connect(self.db_file_path)
        db_cursor = db_connection.cursor()
        db_cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
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
            return
        
        db_cursor.execute('''CREATE TABLE IF NOT EXISTS routes (route_id TEXT, from_port TEXT, to_port TEXT, leg_duration TEXT, points TEXT)''')

        csv.field_size_limit(1073741824) # 1GB limit
        with open(data_file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                db_cursor.execute('''INSERT INTO routes (route_id, from_port, to_port, leg_duration, points) VALUES (?, ?, ?, ?, ?)''', 
                            (row['route_id'], row['from_port'], row['to_port'], row['leg_duration'], row['points']))

        db_connection.commit()
        db_cursor.close()
        db_connection.close()
        
        
    def get_all_routes(self) -> list:
        db_connection = sqlite3.connect(self.db_file_path)
        db_cursor = db_connection.cursor()
        returnList = []
        
        db_cursor.execute("SELECT route_id, from_port, to_port, leg_duration FROM routes")
        rows = db_cursor.fetchall()
        for row in rows:
            rowDict = {}
            rowDict["route_id"] = row[0]
            rowDict["from_port"] = row[1]
            rowDict["to_port"] = row[2]
            rowDict["leg_duration"] = row[3]
            returnList.append(rowDict)
        
        db_cursor.close()
        db_connection.close()
        return returnList
    
    def get_route(self, route_id) -> list:
        db_connection = sqlite3.connect(self.db_file_path)
        db_cursor = db_connection.cursor()
        
        db_cursor.execute("SELECT route_id, from_port, to_port, leg_duration, points FROM routes WHERE route_id = ?", (route_id,))
        rows = db_cursor.fetchall()
        rowDict = {}
        for row in rows:
            rowDict["route_id"] = row[0]
            rowDict["from_port"] = row[1]
            rowDict["to_port"] = row[2]
            rowDict["leg_duration"] = row[3]
            rowDict["points"] = row[4]
        
        db_cursor.close()
        db_connection.close()
        return rowDict
