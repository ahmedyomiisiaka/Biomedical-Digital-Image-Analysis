from libtiff import TIFF
from matplotlib import pyplot as plt
import numpy as np

tiff_file = TIFF.open("data/ImgSet3/imgset3/Fig0333(a)(test_pattern_blurring_orig).tif", mode="r")
image = tiff_file.read_image()

print("Image shape:", image.shape)
print("Data type:", image.dtype)
print("Minimum intensity:", np.min(image))
print("Maximum intensity:", np.max(image))
print("Mean intensity:", np.mean(image))

plt.imshow(image, cmap="gray", interpolation="nearest", vmin=0, vmax=255)
plt.title("Test pattern - original")
plt.axis("off")
plt.savefig("results/blurring_original.png", dpi=150, bbox_inches="tight")
plt.show()