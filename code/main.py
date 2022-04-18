import os
import geopandas as gpd
from osgeo import gdal
from shapely import geometry
import shutil

def main():
    
    data_dir = os.path.join("..","data")
    
    full_fn = os.path.join(data_dir,"area_oi.shp")
    shapefile = gpd.read_file(full_fn).geometry[0]
    
    raster_fns = [ fn for fn in os.listdir(data_dir) if fn.endswith(".tif")]
    
    intersects_dir = os.path.join(data_dir,"intersects")
    if not os.path.isdir(intersects_dir):
        os.mkdir(intersects_dir)
    
    for idx,fn in enumerate(raster_fns):
        full_fn = os.path.join(data_dir,fn)
        
        geom = geometry.Polygon(gdal.Info(full_fn,format="json")["wgs84Extent"]["coordinates"][0])
        
        intersects = geom.intersects(shapefile)
        print(f"{idx}/{len(raster_fns)};\t\ŧGEOM intersects: ", intersects)
        if intersects:
            shutil.copy(full_fn,os.path.join(intersects_dir,fn))
        
    
    

if __name__=="__main__":
    main()