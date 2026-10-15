from libtiff import TIFF
from matplotlib import pyplot as plt

tiff_file = TIFF.open("data/ImgSet1/imgset1/Region_001_FOV_00041_DAPI_Gray.tif", mode="r")
dapi_image = tiff_file.read_image()
print("Image shape:", dapi_image.shape)
print("Image data type:", dapi_image.dtype)
print("Minimum pixel value:", dapi_image.min())
print("Maximum pixel value:", dapi_image.max())

plt.imshow(dapi_image, cmap="gray", interpolation="nearest", vmin=0, vmax=255)
plt.title("DAPI fluorescence - grayscale")
plt.axis("off")
plt.savefig("results/dapi_grayscale.png", dpi=150, bbox_inches="tight")
plt.show()