from typing import Any, Mapping

import shapely
from networkx import MultiDiGraph, MultiGraph

__all__ = [
    "assertive_add_edge",
    "add_shapely_node",
    "IllegalLoopException",
    "IllegalDuplicateEdgeException",
]


class IllegalLoopException(Exception): ...


class IllegalDuplicateEdgeException(Exception): ...


def assertive_add_edge(
    graph: MultiGraph,
    u: int,
    v: int,
    uniqueid: int,
    attributes: Mapping[str, Any],
    *,
    allow_loops: bool = True,
    allow_duplicates: bool = False,
) -> None:
    """

    :param graph: The Graph
    :type graph: MultiDiGraph
    :param u: from node id
    :type u: int
    :param v: to node id
    :type v: int
    :param uniqueid: id of edge
    :type uniqueid: int
    :param attributes: attributes of edge
    :type attributes: Mapping[str, Any]
    :param allow_loops: Allow loops
    :type allow_loops: bool
    :param allow_duplicates: Allow duplicate edges
    :type allow_duplicates: bool
    :return: None
    """
    if not allow_loops:
        if u == v:
            raise IllegalLoopException(f"{u} == {v}")

    assert isinstance(u, int), f"{u=} is not int, but {type(u)=}"
    assert isinstance(v, int), f"{v=} is not int, but {type(v)=}"

    assert graph.has_node(u)
    assert graph.has_node(v)

    if not allow_duplicates and graph.has_edge(u, v, uniqueid):
        if graph.has_edge(u, v, uniqueid):
            raise IllegalDuplicateEdgeException(
                f"Graph already contains the edge ({u} -> {v}) with {uniqueid=}"
            )

    graph.add_edge(u, v, key=uniqueid, uniqueid=uniqueid, **attributes)


def add_shapely_node(graph: MultiGraph, u: int, point: shapely.Point, **kwargs) -> None:
    """
    Add a shapely point based node to the graph.

    :param graph: The Graph
    :type graph: MultiDiGraph
    :param u: Node id
    :type u: int
    :param point:
    :type point: shapely.Point
    :param kwargs: Attributes of node
    :return: None
    """
    assert isinstance(u, int)

    graph.add_node(
        u,
        x=float(point.x),
        y=float(point.y),
        **kwargs,
    )
