from libtiff import TIFF
from matplotlib import pyplot as plt
import numpy as np

tiff_file = TIFF.open("data/ImgSet2/imgset2/Fig0309(a)(washed_out_aerial_image).tif", mode="r")
image = tiff_file.read_image()
print("Image shape:", image.shape)
print("Image data type:", image.dtype)
print("Minimum intensity:", image.min())
print("Maximum intensity:", image.max())

plt.imshow(image, cmap="gray", interpolation="nearest", vmin=0, vmax=255)
plt.title("Aerial image - original")
plt.axis("off")
plt.savefig("results/aerial_original.png", dpi=150, bbox_inches="tight")
plt.show()