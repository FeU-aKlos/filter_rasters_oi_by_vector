from ast import arg
import os
import geopandas as gpd
from osgeo import gdal
from shapely import geometry
import shutil
from argparse import ArgumentParser
import time
import threading
from math import ceil, cos, pi, radians

def _create_args():
    parser = ArgumentParser()
    parser.add_argument("-d", "--data_directory",dest="data_directory",default=os.path.join("..","data"))
    parser.add_argument("-o", "--output_directory",dest="output_directory",default=os.path.join("..","output"))
    parser.add_argument("-shp", "--shapefile",dest="shapefile",default="area_oi.shp")
    parser.add_argument("-fe", "--file_ending",dest="file_ending",default=".jp2")
    parser.add_argument("-n", "--nr_threads",dest="nr_threads",default=12,type=int)
    
    return parser.parse_args()

def main():
    def task(args,fns):
        for idx,fn in enumerate(fns):
            full_fn = os.path.join(args.data_directory,fn)
            geom = geometry.Polygon(gdal.Info(full_fn,format="json")["wgs84Extent"]["coordinates"][0])
            
            intersects = geom.intersects(shapefile)
            if idx%1000==0:
                print(f"{idx}/{len(fns)};\t\ŧGEOM intersects: ", intersects)
            if intersects:
                shutil.copy(full_fn,os.path.join(intersects_dir,fn))   
    
    
    args = _create_args()
    
    intersects_dir = os.path.join(args.output_directory,"intersects")
    if not os.path.isdir(intersects_dir):
        os.makedirs(intersects_dir)
    
    shapefile = gpd.read_file(args.shapefile)
    shapefile.dropna(inplace=True, subset=["geometry"])
    shapefile.reset_index(drop=True,inplace=True)
    shapefile = shapefile.to_crs("EPSG:4326").geometry[0]
    
    minx, miny, maxx, maxy = shapefile.bounds
    print(minx, miny, maxx, maxy)
    
    def precheck(fn):
        fn = fn[4:-4]
        fn = fn.replace("E", "")
        fn_split = fn.split("_")
        y = float(".".join(fn_split[:2]))
        x = float(".".join(fn_split[2:]))
        
        # print(x, minx, maxx)
        avg_dist_between_lat = 111320
        half_x_width = 1000
        x_ = 1/ avg_dist_between_lat* half_x_width
        earth_circumference = 40075000
        half_circle_in_degrees = 180
        half_y_height = 735
        y_ = 1/(cos(radians(y))*earth_circumference*pi/half_circle_in_degrees)*half_y_height
        # print(x_, y_ )
        if x<minx-x_  or x>maxx+x_:
            return False
        elif y<miny-y_ or y>maxy+y_:
            return False
        
        return True
    
    
    
    raster_fns = [ fn for fn in os.listdir(args.data_directory) if fn.endswith(args.file_ending)]
    
    raster_fns = [fn for fn in raster_fns if precheck(fn)]
    
    
    nr_files = len(raster_fns)
    
    print(f"Found {nr_files} files.")
    
    offset = ceil(nr_files/args.nr_threads)
    raster_fns_split = [raster_fns[x:x+offset] for x in range(0,nr_files,offset)]
    threads = []
    for i in range(args.nr_threads):
        t = threading.Thread(target=task, args=(args,raster_fns_split[i]))
        threads.append(t)
        threads[-1].start()
    
    for t in threads:
        t.join()
    
if __name__=="__main__":
    main()