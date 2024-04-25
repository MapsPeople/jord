#!/usr/bin/env python3
from geopandas import GeoDataFrame, GeoSeries

from jord.qlive_utilities.clients.auto import AutoQliveClient

DEFAULT_CRS = "EPSG:3857"  # "EPSG:4326"
crs = DEFAULT_CRS

server_address = "tcp://localhost:5555"
# server_address = "tcp://10.0.2.81:5555"

with AutoQliveClient(server_address) as qlive:
    df = GeoDataFrame(
        {
            "City": ["Buenos Aires", "Brasilia", "Santiago", "Bogota", "Caracas"],
            "Country": ["Argentina", "Brazil", "Chile", "Colombia", "Venezuela"],
            "layer": ["layer1", "layer2", "layer3", "layer4", "layer5"],
            "geometry": [
                "POINT(-58.66 -34.58)",
                "POINT(-47.91 -15.78)",
                "POINT(-70.66 -33.45)",
                "POINT(-74.08 4.60)",
                "POINT(-66.86 10.48)",
            ],
        }
    )

    df["geometry"] = GeoSeries.from_wkt(df["geometry"])

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

    if False:
        for t in df.iterfeatures():
            print(t)

    print(qlive.add_dataframe_layer(GeoDataFrame(df, geometry="geometry")))

    # qlive.add_dataframe(GeoDataFrame(df, geometry="Coordinates"))
