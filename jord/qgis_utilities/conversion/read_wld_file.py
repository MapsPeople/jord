from pathlib import Path
from typing import Any

# noinspection PyUnresolvedReferences
from qgis.PyQt.QtGui import QTransform

__all__ = ["read_wld_file"]


def read_wld_file(geom: Any, wld_file_path: Path) -> None:
    assert wld_file_path is not None
    assert wld_file_path.exists()

    with open(wld_file_path) as wld_file:
        m32 = (float(c) for c in wld_file.readlines())

        transformer = QTransform(*m32)

        geom.transform(transformer)
