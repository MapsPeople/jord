__all__ = ["load_spatialite"]

import sqlite3


def load_spatialite(dbapi_conn: sqlite3.Connection, *args, **kwargs) -> None:
    dbapi_conn.enable_load_extension(True)
    dbapi_conn.load_extension("mod_spatialite")
