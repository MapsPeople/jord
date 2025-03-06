from jord.qlive_utilities.clients.auto import AutoQliveClient

DEFAULT_CRS = "EPSG:3857"  # "EPSG:4326"
crs = DEFAULT_CRS

example_wkt_polygon = (
    "POLYGON((10.689697265625 -25.0927734375, 34.595947265625 "
    "-20.1708984375, 38.814697265625 -35.6396484375, 13.502197265625 "
    "-39.1552734375, 10.689697265625 -25.0927734375))"
)

example_wkt_gm = (
    "GEOMETRYCOLLECTION(POINT(0 0), LINESTRING(0 0, 1440 900), POLYGON((0 0, 0 1024, 1024 1024, "
    "1024 0, 0 0)))"
)

# server_address = "tcp://localhost:5555"
server_address = "tcp://10.0.2.81:5555"

with AutoQliveClient(server_address) as qlive:
    if True:
        qlive.add_shapely_geometry(
            {"gm1": example_wkt_gm, "poly1": example_wkt_polygon},
        )
