pipeline = """
{
    "pipeline":
        [
            {
                 "type": "readers.las",
                 "filename": "#"
            },
            {
                 "type": "filters.reprojection",
                 "in_srs": "EPSG:2193",
                 "out_srs": "EPSG:2193"
            },
            {
                 "type": "writers.las",
                 "filename": "#",
                 "a_srs": "EPSG:2193",
                 "forward": "all"
            }
        ]
}
"""

pdal_transformation_pipeline = """
[
    "untransformed.las",
    {
        "type":"filters.transformation",
        "matrix":"0 -1  0  1  1  0  0  2  0  0  1  3  0  0  0  1"
    },
    {
        "type":"writers.las",
        "filename":"transformed.las"
    }
]
"""

json = """
[
    "1.2-with-color.las",
    {
        "type": "filters.sort",
        "dimension": "X"
    }
]
"""

import pdal

pipeline = pdal.Pipeline(json)
count = pipeline.execute()
arrays = pipeline.arrays
metadata = pipeline.metadata
log = pipeline.log
