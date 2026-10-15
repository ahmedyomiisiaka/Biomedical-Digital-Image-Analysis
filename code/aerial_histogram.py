from libtiff import TIFF
from matplotlib import pyplot as plt
import numpy as np

tiff_file = TIFF.open("data/ImgSet2/imgset2/Fig0309(a)(washed_out_aerial_image).tif", mode="r")
image = tiff_file.read_image()

histogram = np.bincount(image.ravel(), minlength=256)

print("Total pixels:", image.size)
print("Histogram total:", histogram.sum())
print("Most frequent intensity:", np.argmax(histogram))

intensities = np.arange(256)

plt.figure(figsize=(8, 5))
plt.bar(intensities, histogram, width=1.0, color="gray")
plt.title("Aerial image - original histogram")
plt.xlabel("Intensity")
plt.ylabel("Number of pixels")
plt.xlim(0, 255)
plt.savefig("results/aerial_original_histogram.png", dpi=150, bbox_inches="tight")
plt.show()