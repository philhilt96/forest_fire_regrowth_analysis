import os
import pandas as pd
from osgeo import gdal

def convert_tif_folder_to_csv(folder_name):
    # Get all .tif files
    data_folder = folder_name
    tif_files = os.listdir(data_folder)

    df = pd.DataFrame()

    # loop through files and add to dataframe, adding NBR as last column
    for file in tif_files:
        if not file.endswith('.tif'):
                print('skipping ' + file)
                continue
        try:
            print('opening ' + file)
            # Open the .tif file and get the number of bands
            ds = gdal.Open(os.path.join(data_folder, file))
            num_bands = ds.RasterCount

            # Loop through each band and extract the pixel values
            for i in range(1, num_bands+1):
                band = ds.GetRasterBand(i)
                band_name = file.split('-')[1].rstrip('.tif')
                band_data = band.ReadAsArray()
                print(f'flattening array shape {band_data.shape} to 1D array')
                data = band_data.ravel()
                df[band_name] = data.astype('float32')

            # Close the .tif file
            ds = None
        except Exception as e:
            print(e)

    print(f'saving {data_folder} to .csv')
    print(f'Dataframe shape: {df.shape}')
    print(df.head)
    # Save the pixel values to a .csv file
    df.to_csv(f'{data_folder}.csv', index=False)


# plot normalized values vertically
# columns = ['NBR', 'ARI2', 'ARI1', 'CRI2', 'CSI']
# # Iterate over each column
# for column in columns:
#     min_value = df_copy[column].min()
#     max_value = df_copy[column].max()
#     mean_value = df_copy[column].mean()
#     print(f"{column} - Min: {min_value}, Max: {max_value}, Mean: {mean_value}")
#     nbr = df[column].to_numpy()
#     nbr_matrix = nbr.reshape(2935, 3399)
#     print(type(nbr_matrix[0][0]))
#     plt.figure(figsize=(5, 5))
#     plt.imshow(nbr_matrix, vmin=min_value, vmax=max_value)
#     plt.colorbar()

# plot normalized  values
# Normalized to [0:1] - 'CSI', 'ARI1', 'CRI2'
# Normalized to [-1,1] - 'NBR', 'ARI2'
# Determine the number of rows and columns for subplots
# num_bands = len(band_names)
# num_rows = math.ceil(math.sqrt(num_bands))
# num_cols = math.ceil(num_bands / num_rows)

# # Plot each band in a separate subplot
# fig, axes = plt.subplots(num_rows, num_cols, figsize=(10, 10))
# fig.tight_layout(pad=3.0)  # Adjust spacing between subplots

# for i, band_name in enumerate(band_names):
#     row = i // num_cols
#     col = i % num_cols

#     band = df[band_name].to_numpy()
#     band_matrix = band.reshape(2935, 3399)

#     vmin, vmax = None, None
#     if band_name in ['NBR', 'ARI2']:
#         vmin, vmax = -1, 1
#     elif band_name in ['CSI', 'ARI1', 'CRI2']:
#         vmin, vmax = 0, 1

#     img = axes[row, col].imshow(band_matrix, cmap='jet', vmin=vmin, vmax=vmax)
#     axes[row, col].set_title(band_name)
#     axes[row, col].axis('off')

#     # Add colorbar
#     cbar = fig.colorbar(img, ax=axes[row, col], aspect=30, pad=0.05)
#     cbar.set_label('Value')

# # Remove empty subplots
# if num_bands < num_rows * num_cols:
#     for i in range(num_bands, num_rows * num_cols):
#         fig.delaxes(axes.flatten()[i])

# plt.show()