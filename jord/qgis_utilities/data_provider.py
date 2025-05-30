from enum import Enum

__all__ = ["CommonVectorDataProviderLibEnum"]


class CommonVectorDataProviderLibEnum(Enum):
    memory = "memory"
    postgres = "postgres"


if __name__ == "__main__":

    def auishd(iface) -> None:
        """
        Some services require you to supply your own API key for the services to work.

        For Esri basemaps you will need a valid ArcGIS online subscription to use the maps.
        """
        # noinspection PyUnresolvedReferences
        from qgis.PyQt.QtCore import QSettings

        """
connection_type
connection_name
authcfg
password
referer
url
username
zmax
zmin
"""

        # Sources
        sources = []
        sources.append(
            [
                "connections-xyz",
                "Google Maps",
                "",
                "",
                "",
                "https://mt1.google.com/vt/lyrs=m&x=%7Bx%7D&y=%7By%7D&z=%7Bz%7D",
                "",
                "19",
                "0",
            ]
        )
        sources.append(
            [
                "connections-xyz",
                "Google Satellite",
                "",
                "",
                "",
                "https://mt1.google.com/vt/lyrs=s&x=%7Bx%7D&y=%7By%7D&z=%7Bz%7D",
                "",
                "19",
                "0",
            ]
        )
        sources.append(
            [
                "connections-xyz",
                "Google Terrain",
                "",
                "",
                "",
                "https://mt1.google.com/vt/lyrs=t&x=%7Bx%7D&y=%7By%7D&z=%7Bz%7D",
                "",
                "19",
                "0",
            ]
        )
        sources.append(
            [
                "connections-xyz",
                "Google Terrain Hybrid",
                "",
                "",
                "",
                "https://mt1.google.com/vt/lyrs=p&x=%7Bx%7D&y=%7By%7D&z=%7Bz%7D",
                "",
                "19",
                "0",
            ]
        )
        sources.append(
            [
                "connections-xyz",
                "Google Satellite Hybrid",
                "",
                "",
                "",
                "https://mt1.google.com/vt/lyrs=y&x=%7Bx%7D&y=%7By%7D&z=%7Bz%7D",
                "",
                "19",
                "0",
            ]
        )
        sources.append(
            [
                "connections-xyz",
                "Stamen Terrain",
                "",
                "",
                "Map tiles by Stamen Design, under CC BY 3.0. Data by OpenStreetMap, under ODbL",
                "http://tile.stamen.com/terrain/%7Bz%7D/%7Bx%7D/%7By%7D.png",
                "",
                "20",
                "0",
            ]
        )
        sources.append(
            [
                "connections-xyz",
                "Stamen Toner",
                "",
                "",
                "Map tiles by Stamen Design, under CC BY 3.0. Data by OpenStreetMap, under ODbL",
                "http://tile.stamen.com/toner/%7Bz%7D/%7Bx%7D/%7By%7D.png",
                "",
                "20",
                "0",
            ]
        )
        sources.append(
            [
                "connections-xyz",
                "Stamen Toner Light",
                "",
                "",
                "Map tiles by Stamen Design, under CC BY 3.0. Data by OpenStreetMap, under ODbL",
                "http://tile.stamen.com/toner-lite/%7Bz%7D/%7Bx%7D/%7By%7D.png",
                "",
                "20",
                "0",
            ]
        )
        sources.append(
            [
                "connections-xyz",
                "Stamen Watercolor",
                "",
                "",
                "Map tiles by Stamen Design, under CC BY 3.0. Data by OpenStreetMap, under ODbL",
                "http://tile.stamen.com/watercolor/%7Bz%7D/%7Bx%7D/%7By%7D.jpg",
                "",
                "18",
                "0",
            ]
        )
        sources.append(
            [
                "connections-xyz",
                "Wikimedia Map",
                "",
                "",
                "OpenStreetMap contributors, under ODbL",
                "https://maps.wikimedia.org/osm-intl/%7Bz%7D/%7Bx%7D/%7By%7D.png",
                "",
                "20",
                "1",
            ]
        )
        sources.append(
            [
                "connections-xyz",
                "Wikimedia Hike Bike Map",
                "",
                "",
                "OpenStreetMap contributors, under ODbL",
                "http://tiles.wmflabs.org/hikebike/%7Bz%7D/%7Bx%7D/%7By%7D.png",
                "",
                "17",
                "1",
            ]
        )
        sources.append(
            [
                "connections-xyz",
                "Esri Boundaries Places",
                "",
                "",
                "Requires ArcGIS Onlinesubscription",
                "https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places"
                "/MapServer/tile/%7Bz%7D/%7By%7D/%7Bx%7D",
                "",
                "20",
                "0",
            ]
        )
        sources.append(
            [
                "connections-xyz",
                "Esri Gray (dark)",
                "",
                "",
                "Requires ArcGIS Onlinesubscription",
                "http://services.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Base/MapServer"
                "/tile/%7Bz%7D/%7By%7D/%7Bx%7D",
                "",
                "16",
                "0",
            ]
        )
        sources.append(
            [
                "connections-xyz",
                "Esri Gray (light)",
                "",
                "",
                "Requires ArcGIS Onlinesubscription",
                "http://services.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer"
                "/tile/%7Bz%7D/%7By%7D/%7Bx%7D",
                "",
                "16",
                "0",
            ]
        )
        sources.append(
            [
                "connections-xyz",
                "Esri National Geographic",
                "",
                "",
                "Requires ArcGIS Onlinesubscription",
                "http://services.arcgisonline.com/ArcGIS/rest/services/NatGeo_World_Map/MapServer/tile/%7Bz%7D"
                "/%7By%7D/%7Bx%7D",
                "",
                "12",
                "0",
            ]
        )
        sources.append(
            [
                "connections-xyz",
                "Esri Ocean",
                "",
                "",
                "Requires ArcGIS Onlinesubscription",
                "https://services.arcgisonline.com/ArcGIS/rest/services/Ocean/World_Ocean_Base/MapServer/tile"
                "/%7Bz%7D/%7By%7D/%7Bx%7D",
                "",
                "10",
                "0",
            ]
        )
        sources.append(
            [
                "connections-xyz",
                "Esri Satellite",
                "",
                "",
                "Requires ArcGIS Onlinesubscription",
                "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/%7Bz%7D/%7By"
                "%7D/%7Bx%7D",
                "",
                "17",
                "0",
            ]
        )
        sources.append(
            [
                "connections-xyz",
                "Esri Standard",
                "",
                "",
                "Requires ArcGIS Onlinesubscription",
                "https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/%7Bz%7D"
                "/%7By%7D/%7Bx%7D",
                "",
                "17",
                "0",
            ]
        )
        sources.append(
            [
                "connections-xyz",
                "Esri Terrain",
                "",
                "",
                "Requires ArcGIS Onlinesubscription",
                "https://server.arcgisonline.com/ArcGIS/rest/services/World_Terrain_Base/MapServer/tile/%7Bz%7D"
                "/%7By%7D/%7Bx%7D",
                "",
                "13",
                "0",
            ]
        )
        sources.append(
            [
                "connections-xyz",
                "Esri Transportation",
                "",
                "",
                "Requires ArcGIS Onlinesubscription",
                "https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Transportation/MapServer"
                "/tile/%7Bz%7D/%7By%7D/%7Bx%7D",
                "",
                "20",
                "0",
            ]
        )
        sources.append(
            [
                "connections-xyz",
                "Esri Topo World",
                "",
                "",
                "Requires ArcGIS Onlinesubscription",
                "http://services.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/%7Bz%7D"
                "/%7By%7D/%7Bx%7D",
                "",
                "20",
                "0",
            ]
        )
        sources.append(
            [
                "connections-xyz",
                "OpenStreetMap Standard",
                "",
                "",
                "OpenStreetMap contributors, under ODbL",
                "http://tile.openstreetmap.org/%7Bz%7D/%7Bx%7D/%7By%7D.png",
                "",
                "19",
                "0",
            ]
        )
        sources.append(
            [
                "connections-xyz",
                "OpenStreetMap H.O.T.",
                "",
                "",
                "OpenStreetMap contributors, under ODbL",
                "http://tile.openstreetmap.fr/hot/%7Bz%7D/%7Bx%7D/%7By%7D.png",
                "",
                "19",
                "0",
            ]
        )
        sources.append(
            [
                "connections-xyz",
                "OpenStreetMap Monochrome",
                "",
                "",
                "OpenStreetMap contributors, under ODbL",
                "http://tiles.wmflabs.org/bw-mapnik/%7Bz%7D/%7Bx%7D/%7By%7D.png",
                "",
                "19",
                "0",
            ]
        )
        sources.append(
            [
                "connections-xyz",
                "OpenTopoMap",
                "",
                "",
                "Kartendaten: © OpenStreetMap-Mitwirkende, SRTM | Kartendarstellung: © OpenTopoMap (CC-BY-SA)",
                "https://tile.opentopomap.org/%7Bz%7D/%7Bx%7D/%7By%7D.png",
                "",
                "17",
                "1",
            ]
        )
        sources.append(
            [
                "connections-xyz",
                "Strava All",
                "",
                "",
                "OpenStreetMap contributors, under ODbL",
                "https://heatmap-external-b.strava.com/tiles/all/bluered/%7Bz%7D/%7Bx%7D/%7By%7D.png",
                "",
                "15",
                "0",
            ]
        )
        sources.append(
            [
                "connections-xyz",
                "Strava Run",
                "",
                "",
                "OpenStreetMap contributors, under ODbL",
                "https://heatmap-external-b.strava.com/tiles/run/bluered/%7Bz%7D/%7Bx%7D/%7By%7D.png?v=19",
                "",
                "15",
                "0",
            ]
        )
        sources.append(
            [
                "connections-xyz",
                "Open Weather Map Temperature",
                "",
                "",
                "Map tiles by OpenWeatherMap, under CC BY-SA 4.0",
                "http://tile.openweathermap.org/map/temp_new/%7Bz%7D/%7Bx%7D/%7By%7D.png?APPID={your_API_key}",
                "",
                "19",
                "0",
            ]
        )
        sources.append(
            [
                "connections-xyz",
                "Open Weather Map Clouds",
                "",
                "",
                "Map tiles by OpenWeatherMap, under CC BY-SA 4.0",
                "http://tile.openweathermap.org/map/clouds_new/%7Bz%7D/%7Bx%7D/%7By%7D.png?APPID={your_API_key}",
                "",
                "19",
                "0",
            ]
        )
        sources.append(
            [
                "connections-xyz",
                "Open Weather Map Wind Speed",
                "",
                "",
                "Map tiles by OpenWeatherMap, under CC BY-SA 4.0",
                "http://tile.openweathermap.org/map/wind_new/%7Bz%7D/%7Bx%7D/%7By%7D.png?APPID={your_API_key}",
                "",
                "19",
                "0",
            ]
        )
        sources.append(
            [
                "connections-xyz",
                "CartoDb Dark Matter",
                "",
                "",
                "Map tiles by CartoDB, under CC BY 3.0. Data by OpenStreetMap, under ODbL.",
                "http://basemaps.cartocdn.com/dark_all/%7Bz%7D/%7Bx%7D/%7By%7D.png",
                "",
                "20",
                "0",
            ]
        )
        sources.append(
            [
                "connections-xyz",
                "CartoDb Positron",
                "",
                "",
                "Map tiles by CartoDB, under CC BY 3.0. Data by OpenStreetMap, under ODbL.",
                "http://basemaps.cartocdn.com/light_all/%7Bz%7D/%7Bx%7D/%7By%7D.png",
                "",
                "20",
                "0",
            ]
        )
        sources.append(
            [
                "connections-xyz",
                "Bing VirtualEarth",
                "",
                "",
                "",
                "http://ecn.t3.tiles.virtualearth.net/tiles/a{q}.jpeg?g=1",
                "",
                "19",
                "1",
            ]
        )

        for source in sources:  # Add sources to browser
            connection_type = source[0]
            connection_name = source[1]

            QSettings().setValue(
                f"qgis/{connection_type}/{connection_name}/authcfg", source[2]
            )
            QSettings().setValue(
                f"qgis/{connection_type}/{connection_name}/password", source[3]
            )
            QSettings().setValue(
                f"qgis/{connection_type}/{connection_name}/referer", source[4]
            )
            QSettings().setValue(
                f"qgis/{connection_type}/{connection_name}/url", source[5]
            )
            QSettings().setValue(
                f"qgis/{connection_type}/{connection_name}/username", source[6]
            )
            QSettings().setValue(
                f"qgis/{connection_type}/{connection_name}/zmax", source[7]
            )
            QSettings().setValue(
                f"qgis/{connection_type}/{connection_name}/zmin", source[8]
            )

        iface.reloadConnections()  # Update GUI
