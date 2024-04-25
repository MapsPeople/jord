#!/usr/bin/env python3
from geopandas import GeoSeries
from pandas import DataFrame

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

server_address = "tcp://localhost:5555"
# server_address = "tcp://10.0.2.81:5555"

with AutoQliveClient(server_address) as qlive:
    df = DataFrame(
        {
            "City": ["Buenos Aires", "Brasilia", "Santiago", "Bogota", "Caracas"],
            "Country": ["Argentina", "Brazil", "Chile", "Colombia", "Venezuela"],
            "layer": ["layer1", "layer2", "layer3", "layer4", "layer5"],
            "Coordinates": [
                "POINT(-58.66 -34.58)",
                "POINT(-47.91 -15.78)",
                "POINT(-70.66 -33.45)",
                "POINT(-74.08 4.60)",
                "POINT(-66.86 10.48)",
            ],
        }
    )

    df["Coordinates"] = GeoSeries.from_wkt(df["Coordinates"])

    if False:
        for i, d in df.iterrows():
            for k, v in d.items():
                print(k)
                print(v)
    if False:
        for k, v in df.iteritems():
            print(k)
            print(v)

    if False:
        for t in df.itertuples():
            t
            print(t)

    qlive.add_dataframe_layer(DataFrame(df), geometry_column="Coordinates")
