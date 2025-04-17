# imports
import s3fs
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import datetime
import boto3
import botocore
import pooch
import os
import netCDF4
import h5netcdf

# to access the NDVI data from AWS S3 bucket, we first need to connect to s3 bucket
fs = s3fs.S3FileSystem(anon=True)

date_sel = datetime.datetime(
    2014, 3, 12, 0
)  # select a desired date and hours (midnight is zero)

# automatic filename from data_sel. we use strftime (string format time) to get the text format of the file in question.
file_location = fs.glob(
    "s3://noaa-cdr-ndvi-pds/data/"
    + date_sel.strftime("%Y")
    + "/VIIRS-Land_v001_NPP13C1_S-NPP_*"
    + date_sel.strftime("%Y%m%d")
    + "_c*.nc"
)

file_location


client = boto3.client(
    "s3", config=botocore.client.Config(signature_version=botocore.UNSIGNED)
)  # initialize aws s3 bucket client

filelocation="http://s3.amazonaws.com/" + file_location[0]
filename=file_location[0]

ds = xr.open_dataset(
    pooch.retrieve(
        url= filelocation,
        path=filename,
        known_hash=None
        
    ),
    decode_times=False # to address overflow issue
)  # open the file

ds

# examine NDVI values from the dataset
ndvi = ds.NDVI
ndvi


# figure settings:
# vmin & vmax: minimum and maximum values for the colorbar
# aspect: setting the aspect ratio of the figure, must be combined with `size`
# size: setting the overall size of the figure

# to make plotting faster and less memory intensive we use coarsen to reduce the number of pixels
ndvi.coarsen(latitude=5).mean().coarsen(longitude=5).mean().plot(
    vmin=-0.1,
    vmax=1.0,
    aspect=1.8,
    size=5
)