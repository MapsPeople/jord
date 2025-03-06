import sqlite3

# from pysqlite2 import dbapi2 as sqlite3

# setup an in-memory database
con = sqlite3.connect(":memory:")
# enable loading extensions and load spatialite
con.enable_load_extension(True)
try:
    con.load_extension("mod_spatialite.so")
except sqlite3.OperationalError:
    con.load_extension("libspatialite.so")
