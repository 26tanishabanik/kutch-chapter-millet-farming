
import ee
from google.oauth2 import service_account
from ee import oauth
#import geemap
import numpy as np
import os
import rasterio
from rasterio.mask import mask
import shapely
from shapely.geometry import Polygon,box
import streamlit as st

def get_temperature(start_date, end_date, roi):
  start_date='2013-03-18'
  col = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2').filterDate(start_date, end_date).filterBounds(roi).mean()
  temp  = col.select('ST_B10').multiply(0.00341802).add(149.0).subtract(273.15).rename('temp')
  latlon = ee.Image.pixelLonLat().addBands(temp)
  latlon = latlon.reduceRegion(reducer=ee.Reducer.toList(), geometry=roi, scale=100, tileScale = 16, bestEffort=True)
  data_lst = np.array((ee.Array(latlon.get("temp")).getInfo()))
  return data_lst.min(), data_lst.max()

def get_pH(start_date, end_date, roi):
  start_date = '2017-03-28'
  sentinel = ee.ImageCollection("COPERNICUS/S2_SR").filterBounds(roi).filterDate(start_date,end_date).filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE',10)).mean()
  #print("String" , ee.ImageCollection("COPERNICUS/S2_SR").filterBounds(roi).filterDate(start_date,end_date).filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE',10)).toBands())
  ph  = ee.Image(8.339).subtract(ee.Image(0.827).multiply(sentinel.select('B1').divide(sentinel.select('B8')))).rename('ph')
  latlon = ee.Image.pixelLonLat().addBands(ph)
  # apply reducer to list
  latlon = latlon.reduceRegion(reducer=ee.Reducer.toList(), geometry=roi, scale=100, tileScale = 16, bestEffort=True)
  data_ph = np.array((ee.Array(latlon.get("ph")).getInfo()))
  return data_ph.min(), data_ph.max()

def get_rainfall(start_date, end_date, roi):
  rainfall_dataset = ee.ImageCollection('ECMWF/ERA5_LAND/MONTHLY_AGGR').select('total_precipitation_min')
  rainfall_min = rainfall_dataset.filterDate(start_date, end_date).sum().clip(roi).rename('rainfallMin')
  rainfall_dataset = ee.ImageCollection('ECMWF/ERA5_LAND/MONTHLY_AGGR').select('total_precipitation_max')
  rainfall_max = rainfall_dataset.filterDate(start_date, end_date).sum().clip(roi).rename('rainfallMax')
  latlon = ee.Image.pixelLonLat().addBands(rainfall_min)
  # apply reducer to list
  latlon = latlon.reduceRegion(reducer=ee.Reducer.toList(), geometry=roi, scale=100, tileScale = 16, bestEffort=True)
  # get data into three different arrays
  data_rainfall_min = np.array((ee.Array(latlon.get("rainfallMin")).getInfo()))
  latlon = ee.Image.pixelLonLat().addBands(rainfall_max)
  # apply reducer to list
  latlon = latlon.reduceRegion(reducer=ee.Reducer.toList(), geometry=roi, scale=100, tileScale = 16, bestEffort=True)
  # get data into three different arrays
  data_rainfall_max = np.array((ee.Array(latlon.get("rainfallMax")).getInfo()))
  return data_rainfall_min.mean()*100, data_rainfall_max.mean()*100

def get_windspeed(start_date, end_date, roi):
  wind_speed = ee.ImageCollection('NASA/GSFC/MERRA/flx/2').filter(ee.Filter.date(start_date, end_date)).filterBounds(roi).median()
  wind_speed = wind_speed.select('SPEED').rename('windSpeed')
  latlon = ee.Image.pixelLonLat().addBands(wind_speed)
  # apply reducer to list
  latlon = latlon.reduceRegion(reducer=ee.Reducer.toList(), geometry=roi, scale=30, tileScale = 16, bestEffort=True)
  # get data into three different arrays
  data_wind_speed = np.array((ee.Array(latlon.get("windSpeed")).getInfo()))
  return data_wind_speed.min(), data_wind_speed.max()

def qualityMask(im):
  return im.updateMask(im.select('l2b_quality_flag').eq(1)).updateMask(im.select('degrade_flag').eq(0))

'''def get_canopy_cover(start_date, end_date, roi):
  canopy_cover = ee.ImageCollection('LARSE/GEDI/GEDI02_B_002_MONTHLY').map(qualityMask).filter(ee.Filter.date(start_date, end_date)).filterBounds(roi).median().select('cover').rename("canopyCover")
  latlon = ee.Image.pixelLonLat().addBands(canopy_cover)
  # apply reducer to list
  latlon = latlon.reduceRegion(reducer=ee.Reducer.toList(), geometry=roi, scale=30, tileScale = 16, bestEffort=True)
  print("String",ee.Array(latlon.get("canopyCover")))
  # get data into three different arrays
  data_canopy_cover = np.array((ee.Array(latlon.get("canopyCover")).getInfo()))
  return data_canopy_cover.mean() '''

def get_soil_moisture(start_date, end_date, roi):
  soil_moisture = ee.ImageCollection('NASA_USDA/HSL/SMAP10KM_soil_moisture').filter(ee.Filter.date(start_date, end_date)).select('ssm').mean().rename('ssm')
  latlon = ee.Image.pixelLonLat().addBands(soil_moisture)
  # apply reducer to list
  latlon = latlon.reduceRegion(reducer=ee.Reducer.toList(), geometry=roi, scale=30, tileScale = 16, bestEffort=True)
  # get data into three different arrays
  data_soil_moisture = np.array((ee.Array(latlon.get("ssm")).getInfo()))
  return data_soil_moisture.min(), data_soil_moisture.max()

def get_humidity(start_date, end_date, roi):
  humidity = ee.ImageCollection('NASA/GSFC/MERRA/flx/2').filter(ee.Filter.date(start_date, end_date)).select('QLML').mean().rename('humidity')
  latlon = ee.Image.pixelLonLat().addBands(humidity)
  # apply reducer to list
  latlon = latlon.reduceRegion(reducer=ee.Reducer.toList(), geometry=roi, scale=30, tileScale = 16, bestEffort=True)
  # get data into three different arrays
  data_humidity = np.array((ee.Array(latlon.get("humidity")).getInfo()))
  return data_humidity.min(), data_humidity.max()

def get_elevation(roi):
  elevation = ee.Image('USGS/SRTMGL1_003').clip(roi).rename("elevation")
  #latlon = ee.Image.pixelLonLat().addBands(elevation)
  ## apply reducer to list
  #latlon = latlon.reduceRegion(reducer=ee.Reducer.toList(), geometry=roi, scale=30, tileScale = 16, bestEffort=True)
  # get data into three different arrays
  #data_elevation = np.array((ee.Array(latlon.get("elevation")).getInfo()))
  statistics = elevation.reduceRegion(reducer= ee.Reducer.minMax(), geometry= roi, scale= 5)
  minValue = statistics.getNumber('elevation_min').getInfo()
  maxValue = statistics.getNumber('elevation_max').getInfo()
  #print("minValue:", minValue)
  #print("maxValue:", maxValue)
  return minValue, maxValue

def get_soil_salinity(start_date, end_date, roi):
  # Open the GeoTIFF file
  file_path = 'Soil Salinity.tif'
  dataset = rasterio.open(os.path.abspath((file_path)))
  # Define the bounding box coordinates of the polygon
  poly = Polygon(roi)
  # Create a shapely geometry object for the bounding box
  #bbox = box(min_lon, min_lat, max_lon, max_lat)
  #bbox = box(poly.bounds)
  bbox = box(poly.bounds[0],poly.bounds[1],poly.bounds[2],poly.bounds[3])
  # Perform the clip operation
  clipped, transform = mask(dataset, [bbox], crop=True)
  # Get the statistics of the clipped image
  #average_value = np.mean(clipped)
  min_value = np.min(clipped)
  max_value = np.max(clipped)
  # Print the statistics
  #print("Average Pixel Value:", average_value)
  #print("Minimum Pixel Value:", min_value)
  #print("Maximum Pixel Value:", max_value)
  # Close the dataset
  dataset.close()
  return min_value, max_value

#[ee_keys]
#type = "service_account"
#project_id = "xxx"
#private_key_id = "xxx"
#private_key = "xxx"
#client_email = "xxx"
#client_id = "xxx"
#auth_uri = "xxx"
#token_uri = "xxx"
#auth_provider_x509_cert_url = "xxx"
#client_x509_cert_url = "xxx"

def fetch_satellite_data(start_date, end_date, aoi_roi):
  #service_account_keys = st.secrets["ee_keys"]
  #credentials = service_account.Credentials.from_service_account_info(service_account_keys, scopes=oauth.SCOPES)
  #ee.Initialize(credentials)
  #ee.Authenticate()
  ee.Initialize()
  poly = shapely.geometry.Polygon(aoi_roi[0])
  roi = ee.Geometry.Rectangle([poly.bounds[0],poly.bounds[1],poly.bounds[2],poly.bounds[3]])
  temperature_min, temperature_max = get_temperature(start_date, end_date, roi)
  pH_min, pH_max = get_pH(start_date, end_date, roi)
  rainfall_min, rainfall_max = get_rainfall(start_date, end_date, roi)
  windspeed_min, windspeed_max = get_windspeed(start_date, end_date, roi)
  #canopy_cover_mean = get_canopy_cover(start_date, end_date, roi)
  soil_moisture_min, soil_moisture_max = get_soil_moisture(start_date, end_date, roi)
  humidity_min, humidity_max = get_humidity(start_date, end_date, roi)
  elevation_min, elevation_max = get_elevation(roi)
  soil_salinity_min_value, soil_salinity_max_value = get_soil_salinity(start_date, end_date, aoi_roi[0])
  return temperature_min, temperature_max, pH_min, pH_max, rainfall_min, rainfall_max, windspeed_min, windspeed_max, soil_moisture_min, soil_moisture_max, humidity_min, humidity_max, elevation_min, elevation_max,soil_salinity_min_value, soil_salinity_max_value
