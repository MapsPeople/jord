import pytest
import shapely
from shapely.geometry import box

from jord.shapely_utilities import overlap_groups


def test_3_groups():
    data = [
        box(1, 1, 3, 3),
        box(2, 2, 3, 3),
        box(4, 4, 6, 6),
        box(4, 4, 5, 5),
        box(5, 5, 6, 6),
        box(7, 7, 8, 8),
        box(1, 1, 2, 2),
        box(4, 4, 6, 6),
    ]

    assert len(overlap_groups(data)) == 3


def test_3_groups_unique():
    data = [
        box(1, 1, 3, 3),
        box(2, 2, 3, 3),
        box(4, 4, 6, 6),
        box(4, 4, 5, 5),
        box(5, 5, 6, 6),
        box(7, 7, 8, 8),
        box(1, 1, 2, 2),
        box(4, 4, 6, 6),
    ]

    assert len(overlap_groups(data, must_be_unique=True)) == 3


def test_in_both():
    data = [
        box(1, 1, 3, 3),
        shapely.unary_union([box(2, 2, 3, 3), box(4, 4, 5, 5)]),
        box(4, 4, 6, 6),
        box(4, 4, 5, 5),
    ]

    assert len(overlap_groups(data)) == 2

    # pprint(overlap_groups(data, must_be_unique=True)) # FAILS!


def test_multi_polygon_in_both_enforce_unique():
    data = [
        box(1, 1, 3, 3),
        shapely.unary_union([box(2, 2, 3, 3), box(4, 4, 5, 5)]),
        box(4, 4, 6, 6),
        box(4, 4, 5, 5),
    ]

    with pytest.raises(AssertionError):
        overlap_groups(data, must_be_unique=True)


def test_in_both_transistive():
    data = [
        box(1, 1, 3, 3),
        shapely.convex_hull(shapely.unary_union([box(2, 2, 3, 3), box(4, 4, 5, 5)])),
        box(4, 4, 6, 6),
        box(4, 4, 5, 5),
    ]

    assert len(overlap_groups(data)) == 1


def test_in_both_transistive_enforce_unique():
    data = [
        box(1, 1, 3, 3),
        shapely.convex_hull(shapely.unary_union([box(2, 2, 3, 3), box(4, 4, 5, 5)])),
        box(4, 4, 6, 6),
        box(4, 4, 5, 5),
    ]

    assert len(overlap_groups(data, must_be_unique=True)) == 1


if __name__ == "__main__":
    test_3_groups()
    test_3_groups_unique()
    test_in_both()
    test_multi_polygon_in_both_enforce_unique()
    test_in_both_transistive()
    test_in_both_transistive_enforce_unique()
