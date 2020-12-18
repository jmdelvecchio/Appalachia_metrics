import os
from appalachia_metrics_script import metrics_execute

#for file in os.listdir("."):
#	if file.endswith(".tif"):
#		print((os.path.join(".", file)))
#		RasterFile=file
#		#RasterFile="./base_tifs/"+file
#		import appalachia_metrics_script
for fname in os.listdir("."):
	if ".tif" in fname and "UTM" not in fname:
		print("Running script on" + (os.path.join(".", fname)))
		metrics_execute(fname)
#		RasterFile=fname
#		print("Post-Raster-file-definition"+fname)
#		import appalachia_metrics_script
