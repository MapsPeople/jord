__author__ = "heider"
__doc__ = r"""

           Created on 5/5/22
           """

from PIL.TiffTags import TAGS, TAGS_V2
from warg import invert_dict, pivot_dict_object

__all__ = ["TIFF_TAG_IDS", "TIFF_TAG_V2_IDS"]

TIFF_TAG_IDS = invert_dict(TAGS)

# TIFF_TAG_V2_IDS = invert_dict(TAGS_V2) # NOT hashable value types
TIFF_TAG_V2_IDS = pivot_dict_object(TAGS_V2, "name")

if __name__ == "__main__":
    print(TIFF_TAG_IDS)
    print(TIFF_TAG_V2_IDS)
