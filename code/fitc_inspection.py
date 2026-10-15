from libtiff import TIFF
from matplotlib import pyplot as plt

tiff_file = TIFF.open("data/ImgSet1/imgset1/Region_001_FOV_00041_FITC_Gray.tif", mode="r")
fitc_image = tiff_file.read_image()
print("Image shape:", fitc_image.shape)
print("Image data type:", fitc_image.dtype)
print("Minimum pixel value:", fitc_image.min())
print("Maximum pixel value:", fitc_image.max())

plt.imshow(fitc_image, cmap="gray", interpolation="nearest", vmin=0, vmax=255)
plt.title("FITC fluorescence - grayscale")
plt.axis("off")
plt.savefig("results/fitc_grayscale.png", dpi=150, bbox_inches="tight")
plt.show()