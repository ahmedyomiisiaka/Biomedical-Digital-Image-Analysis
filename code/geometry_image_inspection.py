from libtiff import TIFF
import numpy as np

tiff_file = TIFF.open("data/ImgSet4/imgset4/Pattern64.tif", mode="r")
image = tiff_file.read_image()

print("Image shape:", image.shape)
print("Data type:", image.dtype)
print("Minimum pixel value:", np.min(image))
print("Maximum pixel value:", np.max(image))