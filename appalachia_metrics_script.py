import lsdtopytools as lsd
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import lsdttparamselector as ps
import lsdviztools.lsdbasemaptools as bmt
from lsdviztools.lsdplottingtools import lsdmap_gdalio as gio
import lsdviztools.lsdmapwrappers as lsdmw
import lsdttparamselector as ps
import rasterio
from osgeo import gdal
#%matplotlib inline






def metrics_execute(RasterFile):
    DataDirectory = "./"
    #RasterFile = "hunt.tif"
    position=RasterFile.index('.')
    filename=RasterFile[0:position]
    gio.convert4lsdtt(DataDirectory, RasterFile,minimum_elevation=0.01,resolution=3)

    lsdtt_parameters = {"surface_fitting_radius" : "3",
                        "print_slope" : "true",
                        "print_curvature" : "true",
                        "print_dinf_drainage_area_raster": "true"}
    lsdtt_drive = lsdmw.lsdtt_driver(read_prefix = filename + "_UTM",
                                     write_prefix= filename + "_UTM",
                                     read_path = "./",
                                     write_path = "./",
                                     parameter_dictionary=lsdtt_parameters)
    lsdtt_drive.print_parameters()


    lsdtt_drive.run_lsdtt_command_line_tool()

    filename + '_SLOPE.tif'

    kwargs = {
        'format': 'GTiff',
        'outputType': gdal.GDT_Float32
    }
    #    'outputType': gdal.GDT_Int16

    _ = gdal.Translate(filename + '_SLOPE.tif',filename + '_UTM_SLOPE.bil',**kwargs)
    _ = gdal.Translate(filename + '_CURV.tif',filename + '_UTM_CURV.bil',**kwargs)
    _ = gdal.Translate(filename + '_dinf_area.tif',filename + '_UTM_dinf_area.bil',**kwargs)
    # ds = None

    import fiona
    import rasterio
    import rasterio.mask

    darea = rasterio.open(filename + '_dinf_area.tif')
    curve = rasterio.open(filename + '_CURV.tif')
    slope = rasterio.open(filename + '_SLOPE.tif')
    elev = rasterio.open(filename + '.tif')
    msk_d = darea.read_masks()
    darea_data = darea.read(1, masked=True)
    curve_data = curve.read(1, masked=True)
    slope_data = slope.read(1, masked=True)
    darea_array=darea_data.flatten()
    curve_array=curve_data.flatten()
    slope_array=slope_data.flatten()

    plt.imshow(slope.read(1), vmin=0, vmax=1)
    plt.colorbar()
    plt.title(filename)
    plt.savefig(filename + '_slope.png')

    #Bin edges go by 10 until 1000 m^2
    a1=10.**(np.arange(3, 7)) 
    a2 = np.arange(1,10,1)
    a3 = np.arange(0,1000,10)
    bin_edges = np.append(a3, (np.outer(a1, a2).flatten()))


    from scipy.stats import binned_statistic

    med_stat_ca = binned_statistic(darea_array,curve_array,
                                statistic='median',
                                bins=bin_edges)

    med_stat_sa = binned_statistic(darea_array,slope_array,
                                statistic='median',
                                bins=bin_edges)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(4,3), sharex=True)
    ax1.scatter(med_stat_ca.bin_edges[:-1],med_stat_ca.statistic)
    ax2.scatter(med_stat_sa.bin_edges[:-1],med_stat_sa.statistic)
    ax1.set_xscale('log')
    ax1.set_xlim(1e1, 1e6)

    with fiona.open("Tuscarora.shp", "r") as shapefile:
        Tuscarora_mask = [feature["geometry"] for feature in shapefile]

    out_image, out_transform = rasterio.mask.mask(slope, Tuscarora_mask, crop=True)
    out_meta = slope.meta
    out_meta.update({"driver": "GTiff",
                      "height": out_image.shape[1],
                      "width": out_image.shape[2],
                      "transform": out_transform})

    slope_tusc, out_transform = rasterio.mask.mask(slope, Tuscarora_mask, crop=True)
    out_meta = slope.meta
    out_meta.update({"driver": "GTiff",
                      "height": out_image.shape[1],
                      "width": out_image.shape[2],
                      "transform": out_transform})

    curve_tusc, out_transform = rasterio.mask.mask(curve, Tuscarora_mask, crop=True)
    out_meta = slope.meta
    out_meta.update({"driver": "GTiff",
                      "height": out_image.shape[1],
                      "width": out_image.shape[2],
                      "transform": out_transform})
    darea_tusc, out_transform = rasterio.mask.mask(darea, Tuscarora_mask, crop=True)
    out_meta = slope.meta
    out_meta.update({"driver": "GTiff",
                      "height": out_image.shape[1],
                      "width": out_image.shape[2],
                      "transform": out_transform})

    darea_t_array=darea_tusc.flatten()
    curve_t_array=curve_tusc.flatten()
    slope_t_array=slope_tusc.flatten()

    med_stat_t_ca = binned_statistic(darea_t_array,curve_t_array,
                                statistic='median',
                                bins=bin_edges)

    med_stat_t_sa = binned_statistic(darea_t_array,slope_t_array,
                                statistic='median',
                                bins=bin_edges)


    slope_ntusc, out_transform = rasterio.mask.mask(slope, Tuscarora_mask, invert=True)
    out_meta = slope.meta
    out_meta.update({"driver": "GTiff",
                      "height": out_image.shape[1],
                      "width": out_image.shape[2],
                      "transform": out_transform})

    curve_ntusc, out_transform = rasterio.mask.mask(curve, Tuscarora_mask, invert=True)
    out_meta = curve.meta
    out_meta.update({"driver": "GTiff",
                      "height": out_image.shape[1],
                      "width": out_image.shape[2],
                      "transform": out_transform})
    darea_ntusc, out_transform = rasterio.mask.mask(darea, Tuscarora_mask, invert=True)
    out_meta = darea.meta
    out_meta.update({"driver": "GTiff",
                      "height": out_image.shape[1],
                      "width": out_image.shape[2],
                      "transform": out_transform})
    # with rasterio.open("Tusc_masked.tif", "w", **out_meta) as dest:
    #     dest.write(out_image)
    darea_nt_array=darea_ntusc.flatten()
    curve_nt_array=curve_ntusc.flatten()
    slope_nt_array=slope_ntusc.flatten()
    med_stat_nt_ca = binned_statistic(darea_nt_array,curve_nt_array,
                                statistic='median',
                                bins=bin_edges)

    med_stat_nt_sa = binned_statistic(darea_nt_array,slope_nt_array,
                                statistic='median',
                                bins=bin_edges)

    max_slope_t = max(med_stat_t_sa.statistic.tolist())
    max_slope_da_t = med_stat_t_sa.bin_edges[med_stat_t_sa.statistic.tolist().index(max_slope_t)]
    print(max_slope_da_t)
    max_slope_nt = max(med_stat_nt_sa.statistic.tolist())
    max_slope_da_nt = med_stat_nt_sa.bin_edges[med_stat_nt_sa.statistic.tolist().index(max_slope_nt)]
    print(max_slope_da_nt)

    import pandas as pd



    df = pd.DataFrame(list(zip(bin_edges[1:],med_stat_sa.statistic.tolist(),med_stat_ca.statistic.tolist(),
                            med_stat_t_sa.statistic.tolist(),med_stat_t_ca.statistic.tolist(),
                            med_stat_nt_sa.statistic.tolist(),med_stat_nt_ca.statistic.tolist())),
                   columns = ['Bin', 'Slp_all', 'Curv_all', 'Slp_tusc', 'Curv_tusc', 'Slp_ntsc', 'Curv_ntusc'])

    ds = gdal.Open(RasterFile)
    df['topleftx'] = np.array(ds.GetGeoTransform()[0], dtype=np.float32)
    df['toplefty']  = np.array(ds.GetGeoTransform()[3], dtype=np.float32)
    df['ref']  = ds.GetProjection()[0:45]


    df.to_csv(filename + '_stats.csv',columns=df.columns, index=False)

    import os
    for file in os.listdir("."):
        if file.endswith(".bil"):
            os.remove((os.path.join(".", file)))
        if file.endswith(".hdr"):
            os.remove((os.path.join(".", file)))









