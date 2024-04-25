#!/usr/bin/env python3
import shapely
from geopandas import GeoDataFrame

from jord.qlive_utilities.clients.auto import AutoQliveClient

with AutoQliveClient("5555") as qlive:
    df = GeoDataFrame(
        {
            "City": ["Buenos Aires", "Brasilia", "Santiago", "Bogota", "Caracas"],
            "Country": ["Argentina", "Brazil", "Chile", "Colombia", "Venezuela"],
            "layer": ["layer1", "layer2", "layer3", "layer4", "layer5"],
            "geometry": [
                shapely.from_wkt("POINT(-58.66 -34.58)"),
                shapely.from_wkt("POINT(-47.91 -15.78)"),
                shapely.difference(
                    shapely.from_wkt("POINT(-70.66 -33.45)").buffer(1),
                    shapely.from_wkt("POINT(-70.66 -33.45)")
                    .buffer(0.5)
                    .exterior.buffer(0.1),
                ),  # Multipolygon
                shapely.from_wkt("POINT(-74.08 4.60)").buffer(1).exterior,  # Linestring
                shapely.from_wkt("POINT(-66.86 10.48)").buffer(1),  # Polygon
            ],
        },
        geometry="geometry",
    )

    print(qlive.add_dataframe_layer(df))
