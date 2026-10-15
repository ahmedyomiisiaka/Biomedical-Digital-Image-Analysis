from libtiff import TIFF
from matplotlib import pyplot as plt
import numpy as np

folder = "data/ImgSet1/imgset1/"

acridine_file = TIFF.open(folder + "Region_001_FOV_00041_Acridine_Or_Gray.tif", mode="r")
acridine_image = acridine_file.read_image()

fitc_file = TIFF.open(folder + "Region_001_FOV_00041_FITC_Gray.tif", mode="r")
fitc_image = fitc_file.read_image()

dapi_file = TIFF.open(folder + "Region_001_FOV_00041_DAPI_Gray.tif", mode="r")
dapi_image = dapi_file.read_image()

print("Acridine Orange shape:", acridine_image.shape)
print("FITC shape:", fitc_image.shape)
print("DAPI shape:", dapi_image.shape)

if not (acridine_image.shape == fitc_image.shape == dapi_image.shape):
    raise ValueError("The three images do not have the same shape.")

rgb_image = np.zeros((1024, 1392, 3), dtype=np.uint8)

# Acridine Orange -> red, FITC -> green, DAPI -> blue
rgb_image[:, :, 0] = acridine_image
rgb_image[:, :, 1] = fitc_image
rgb_image[:, :, 2] = dapi_image

print("Composite shape:", rgb_image.shape)
print("Composite data type:", rgb_image.dtype)

plt.imshow(rgb_image, interpolation="nearest")
plt.title("Fluorescence RGB composite")
plt.axis("off")
plt.savefig("results/fluorescence_rgb_composite.png", dpi=150, bbox_inches="tight")
plt.show()