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
import tempfile