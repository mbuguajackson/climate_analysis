# Imports
import s3fs
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import datetime
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings("ignore")

# Connect to the AWS S3 public bucket
fs = s3fs.S3FileSystem(anon=True)

# Select a specific date
date_sel = datetime.datetime(2014, 3, 12, 0)

# Search for file based on the date
file_location = fs.glob(
    "s3://noaa-cdr-ndvi-pds/data/"
    + date_sel.strftime("%Y")
    + "/VIIRS-Land_v001_NPP13C1_S-NPP_*"
    + date_sel.strftime("%Y%m%d")
    + "_c*.nc"
)

if not file_location:
    print("No file found for the selected date.")
else:
    print("File found:", file_location[0])
    
    # Open the file using xarray with s3fs
    with fs.open(file_location[0], 'rb') as f:
        ds = xr.open_dataset(f)

    # Extract NDVI data
    ndvi = ds['NDVI'].squeeze()
    
    # Subset to Kenya bounding box (approx: lat -5 to 5, lon 33 to 42)
    ndvi_kenya = ndvi.sel(lat=slice(5, -5), lon=slice(33, 42))

    # Plotting
    plt.figure(figsize=(8, 6))
    ax = plt.axes(projection=ccrs.PlateCarree())
    ndvi_kenya.plot(ax=ax, transform=ccrs.PlateCarree(), cmap='YlGn', cbar_kwargs={'label': 'NDVI'})
    ax.coastlines()
    ax.set_extent([33, 42, -5, 5])  # zoom to Kenya
    ax.set_title(f"NDVI over Kenya on {date_sel.strftime('%Y-%m-%d')}")
    plt.show()
