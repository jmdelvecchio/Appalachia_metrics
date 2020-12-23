import rasterio
from osgeo import gdal
from matplotlib import pyplot as plt
import numpy as np
import fiona
import rasterio
import rasterio.mask

def dem_tile_extractor(fname, vr_3m):
    # Get DEM number cause we're gonna call the final DEM that
    position=fname.index('.')
    dem_number=fname[0:position]
    print("Now extracting DEM number: " + dem_number)
    
    with fiona.open(fname, "r") as shapefile:
        tile_mask = [feature["geometry"] for feature in shapefile]

    tile_dem, out_transform = rasterio.mask.mask(vr_3m, tile_mask, crop=True)
    out_meta = vr_3m.meta
    out_meta.update({"driver": "GTiff",
                      "height": tile_dem.shape[1],
                      "width": tile_dem.shape[2],
                      "transform": out_transform})

    with rasterio.open("tile_" + dem_number + '.tif', 'w', **out_meta) as dst:
        dst.write(tile_dem)
