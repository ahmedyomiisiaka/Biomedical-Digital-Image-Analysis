from libtiff import TIFF
import numpy as np

path = "data/raw/ImgSetCa2/Kidney1-Crop.tif"

tif = TIFF.open(path, mode="r")
image = tif.read_image()
tif.close()

print("Image shape:", image.shape)
print("Data type:", image.dtype)
print("Minimum intensity:", np.min(image))
print("Maximum intensity:", np.max(image))