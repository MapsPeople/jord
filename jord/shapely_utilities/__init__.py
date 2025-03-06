__author__ = "heider"
__doc__ = r"""

           Created on 1/23/23
           """

from pathlib import Path

with open(Path(__file__).parent / "README.md") as this_init_file:
    __doc__ += this_init_file.read()

from .base import *
from .clamp import *
from .lines import *
from .morphology import *
from .points import *
from .polygons import *
from .geometry_types import *
from .projection import *
from .transformation import *
from .rings import *
from .selection import *
from .grouping import *
from .mirroring import *
from .selection import *
from .uniformity import *
from .subdivision import *
