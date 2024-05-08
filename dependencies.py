from typing import Annotated

from fastapi import Depends

from postgresql_control import PostgreSQLControl
from sqlite_control import SQLiteControl


def get_sqlite_control() -> SQLiteControl:
    return SQLiteControl()


SQLiteRepository = Annotated[SQLiteControl, Depends(get_sqlite_control)]


def get_postgreSQL_control() -> PostgreSQLControl:
    return PostgreSQLControl()


PostgreSQLRepository = Annotated[PostgreSQLControl, Depends(get_postgreSQL_control)]
