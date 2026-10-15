from libtiff import TIFF
from matplotlib import pyplot as plt

tiff_file = TIFF.open("results/tma_rgb_converted.tif", mode="r")
rgba_image = tiff_file.read_image()
print("Image shape:", rgba_image.shape)
print("Image data type:", rgba_image.dtype)
print("Minimum pixel value:", rgba_image.min())
print("Maximum pixel value:", rgba_image.max())

plt.imshow(rgba_image[:, :, :3], interpolation="nearest", vmin=0, vmax=255)
plt.title("TMA2 - RGB converted image")
plt.axis("off")
plt.savefig("results/tma_rgb_corrected.png", dpi=150, bbox_inches="tight")
plt.show()