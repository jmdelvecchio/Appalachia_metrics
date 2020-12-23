import os
import rasterio

import rasterio
from osgeo import gdal
from matplotlib import pyplot as plt
import numpy as np
import fiona
import rasterio
import rasterio.mask

from extraction_function import dem_tile_extractor

# Only read the big honkin DEM once and pass it to each extraction function??
vr_3m = rasterio.open("vridge_3m_18N.tif")

for fname in os.listdir("."):
        if ".shp" in fname and "Tuscarora" not in fname:
                print("Extracting my tile mask on " + (os.path.join(".", fname)))
                dem_tile_extractor(fname, vr_3m) #Right? gotta pass it these two things?
