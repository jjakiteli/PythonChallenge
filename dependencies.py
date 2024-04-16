from typing import Annotated
from fastapi import Depends

from sqlite_control import SQLiteControl

def get_sqlite_control() -> SQLiteControl:
    return SQLiteControl()

SQLiteRepository = Annotated[SQLiteControl, Depends(get_sqlite_control)]

