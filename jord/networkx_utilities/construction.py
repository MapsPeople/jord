import shapely
from networkx import MultiDiGraph

__all__ = ["assertive_add_edge", "add_shapely_node"]


def assertive_add_edge(
    graph: MultiDiGraph, u: int, v: int, uniqueid: int, **kwargs
) -> None:
    if True:  # disallow_loops: bool
        assert u != v, f"{u} == {v}"

    assert isinstance(u, int)
    assert isinstance(v, int)

    assert graph.has_node(u)
    assert graph.has_node(v)

    if graph.has_edge(u, v, uniqueid):
        return
    # assert not graph.has_edge(u,v,uniqueid)

    graph.add_edge(u, v, key=uniqueid, uniqueid=uniqueid, **kwargs)


def add_shapely_node(
    graph: MultiDiGraph, u: int, point: shapely.Point, **kwargs
) -> None:
    assert isinstance(u, int)

    graph.add_node(
        u,
        lon=point.x,
        lat=point.y,
        x=point.x,
        y=point.y,
        # altitude=inter_.location.geoLocation.altitude,
        **kwargs,
    )