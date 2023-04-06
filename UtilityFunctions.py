import matplotlib.pyplot as plt
from osgeo import gdal

# return the NDVI band raw pixels as an array
def get_ndvi_band_pixels(hdf_file):
    # open file and open NDVI subset and get relevant meta data
    raw_data = gdal.Open(hdf_file, gdal.GA_ReadOnly)
    subdataset = gdal.Open(raw_data.GetSubDatasets()[0][0], gdal.GA_ReadOnly)
    ndvi_metadata = subdataset.GetMetadata()
    # ndvi_fill_value = int(ndvi_metadata['_FillValue'])
    nvdi_scale_factor = int(ndvi_metadata['scale_factor'])
    # convert to array - will be NxN pixel size matrix
    band = subdataset.GetRasterBand(1)
    data = band.ReadAsArray()
    scaled_data = data / nvdi_scale_factor
    # close safely
    raw_data = None
    subdataset = None

    return scaled_data

# function not working - don't import
def pre_process_hdf(hdf_file):
  # Open the MOD13A3 hdf file, use full file path
  raw_data = gdal.Open(hdf_file, gdal.GA_ReadOnly)
  subdatasets = raw_data.GetSubDatasets()

  # select the subdataset containing NDVI data
  ndvi_subdataset = None
  for subdataset in subdatasets:
      if "NDVI" in subdataset[0]:
          ndvi_subdataset = subdataset[0]
          break
  # open ndvi subset and subset out the bounding affected area rectangle
  ndvi_raw_dataset = gdal.Open(ndvi_subdataset, gdal.GA_ReadOnly)

  # get metadata variables
  ndvi_metadata = ndvi_raw_dataset.GetMetadata()
  # footprint boundary GPS coordinates
  boundary_n = float(ndvi_metadata['NORTHBOUNDINGCOORDINATE'])
  boundary_s = float(ndvi_metadata['SOUTHBOUNDINGCOORDINATE'])
  boundary_e = float(ndvi_metadata['EASTBOUNDINGCOORDINATE'])
  boundary_w = float(ndvi_metadata['WESTBOUNDINGCOORDINATE'])
  # values to calculate true NDVI from raw data
  ndvi_fill_value = int(ndvi_metadata['_FillValue'])
  nvdi_scale_factor = int(ndvi_metadata['scale_factor'])

  # convert to np array
  ndvi_raw_data = ndvi_raw_dataset.ReadAsArray()

  # NDVI from raw data, ndvi = (ndvi_raw - ndvi_fill) / ndvi_scale
  ndvi_data = ndvi_raw_data / nvdi_scale_factor

  # close the datasets
  ndvi_dataset = None
  hdf_file = None

  # get the effected fire area from spacial GPS rectangle
  n, m = ndvi_data.shape
  spatial_n, spatial_s, spatial_e, spatial_w = (39.22, 37.66, -119.57, -120.81)
  # Transopse the spacial data from the bounding box - needs to be fixed
  row_start = int((boundary_n - spatial_n) / (boundary_n - boundary_s) * n)
  row_end = int((boundary_n - spatial_s) / (boundary_n - boundary_s) * n)
  col_start = int((spatial_w - boundary_w) / (boundary_e - boundary_w) * m)
  col_end = int((spatial_e - boundary_w) / (boundary_e - boundary_w) * m)
  # Extract the smaller area of the NDVI array
  spacial_ndvi_data = ndvi_data[row_start:row_end, col_start:col_end]

  # ndvi_mean = np.mean(spacial_ndvi_data)
  # ndvi_std = np.std(spacial_ndvi_data)
  # ndvi_skew = sp.stats.skew(spacial_ndvi_data)

  # get x and y values from ndvi dataset
  # x, y = np.meshgrid(range(spacial_ndvi_data.shape[1]), range(spacial_ndvi_data.shape[0]))
  # convert numpy array to dataframe
  # cleaned_ndvi_dataset = np.stack([spacial_ndvi_data, np.full_like(spacial_ndvi_data,ndvi_mean), np.full_like(spacial_ndvi_data,ndvi_std), np.full_like(spacial_ndvi_data,ndvi_skew), x, y], axis=2)
  # cleaned_ndvi_reshaped = cleaned_ndvi_dataset.reshape(-1, 6)

  # Calculate RTI using Theil-Sen's estimator
  # Call function to calculate RTI
  # rti_data = rti(ndvi_data)

  # return ndvi_raw_data
  return spacial_ndvi_data
  # return pd.DataFrame(cleaned_ndvi_reshaped, columns=['NDVI', 'mean', 'std', 'skew', 'x', 'y'])