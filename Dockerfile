# FROM skynet1010/filter_rasters_by_vector:v0.0.3
# #FROM ubuntu:20.04

# #RUN apt update; DEBIAN_FRONTEND=noninteractive TZ=Europe/Berlin apt install apt python3-pip cmake build-essential libproj-dev git libgeos-dev libtiff-dev swig vim wget libgeotiff-dev libcurl4-openssl-dev liblaszip-dev ninja-build gdal-bin libgdal-dev -y
# RUN apt update; DEBIAN_FRONTEND=noninteractive TZ=Europe/Berlin apt install apt gdal-bin libgdal-dev -y

# RUN pip install geopandas
# # RUN git clone https://github.com/FeU-aKlos/gdal.git; cd gdal; mkdir build; cd build; cmake .. -DCMAKE_BUILD_TYPE=Release; cmake --build . -j 8; cmake --install .; ldconfig; cd ../swig/python; python3 setup.py build; python3 setup.py install;
# # RUN wget https://github.com/PDAL/PDAL/releases/download/2.3.0/PDAL-2.3.0-src.tar.gz; tar -xf PDAL-2.3.0-src.tar.gz; cd PDAL-2.3.0-src; mkdir build; cd build; cmake .. -DCMAKE_BUILD_TYPE=Release; cmake --build . -j 8;cmake --install .; 
# # RUN  wget https://github.com/pybind/pybind11/archive/refs/tags/v2.9.1.tar.gz; tar -xf v2.9.1.tar.gz; cd pybind11-2.9.1; mkdir build; cd build; cmake .. -DCMAKE_BUILD_TYPE=Release; python3 -m pip install pytest; cmake --build . -j 8; cmake --install .; cd ..; python3 setup.py build; python3 setup.py install;
# # RUN git clone https://github.com/PDAL/python pdalextension; cd pdalextension/; python3 setup.py build; python3 setup.py install;  pip install pdal; ldconfig

# COPY code /app
# WORKDIR /app

# CMD ["python","main.py"]


FROM ubuntu:20.04

WORKDIR /root


ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && apt upgrade -y && apt install -y \
    build-essential \
    cmake \
    git \
    libboost-all-dev \
    libssl-dev \
    libzmq3-dev \
    pkg-config \
    python3 \
    python3-pip \
    python3-setuptools \
    python3-wheel \
    wget 


RUN apt install -y libproj-dev libopenjp2-7-dev

RUN wget https://github.com/OSGeo/gdal/releases/download/v3.8.2/gdal-3.8.2.tar.gz && \
    tar -xvf gdal-3.8.2.tar.gz && \
    cd gdal-3.8.2 && \
    mkdir build && \
    cd build && \
    cmake .. && \
    cmake --build . -j 8 && \
    cmake --build . --target install && \
    ldconfig && \
    cd ../.. && \
    rm -rf gdal-3.8.2.tar.gz gdal-3.8.2

RUN apt install libpq-dev -y

RUN pip install geopandas psycopg2 gdal==3.8.2

CMD [ "python3", "code/main.py", "-db", "geo20231224", "-cptn", "centerpoints_oi", "-u", "postgres", "-pw", "dyab9p38", "-tdir", "/data"]
