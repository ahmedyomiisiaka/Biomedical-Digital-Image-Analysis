from libtiff import TIFF
from matplotlib import pyplot as plt
import numpy as np

tiff_file = TIFF.open("data/ImgSet2/imgset2/Fig0309(a)(washed_out_aerial_image).tif", mode="r")
image = tiff_file.read_image()

histogram = np.bincount(image.ravel(), minlength=256)

cdf = np.cumsum(histogram)

lut = np.round(255 * cdf / image.size).astype(np.uint8)

print("Number of LUT entries:", lut.size)
print("Original image pixels:", image.size)
print("LUT memory in bytes:", lut.nbytes)
print("Original image memory in bytes:", image.nbytes)

print("Total pixels:", image.size)
print("CDF at intensity 0:", cdf[0])
print("CDF at intensity 100:", cdf[100])
print("CDF at intensity 213:", cdf[213])
print("CDF at intensity 255:", cdf[255])

print("LUT at intensity 0:", lut[0])
print("LUT at intensity 100:", lut[100])
print("LUT at intensity 213:", lut[213])
print("LUT at intensity 255:", lut[255])

example_pixels = np.array([0, 100, 213, 255])
print("LUT for example pixels:", lut[example_pixels])

equalized_image = lut[image]

print("Original mean:", image.mean())
print("Equalized mean:", equalized_image.mean())
print("Equalized shape:", equalized_image.shape)
print("Equalized data type:", equalized_image.dtype)
print("Original pixel (100,100):", image[100, 100])
print("Equalized pixel (100,100):", equalized_image[100, 100])

equalized_hist = np.bincount(equalized_image.ravel(), minlength=256)

print("Original histogram total:", histogram.sum())
print("Equalized histogram total:", equalized_hist.sum())

print("Original occupied intensity levels:", np.count_nonzero(histogram))
print("Equalized occupied intensity levels:", np.count_nonzero(equalized_hist))

plt.imsave("results/aerial_equalized.png", equalized_image, cmap="gray", vmin=0, vmax=255)

fig, axes = plt.subplots(1, 2, figsize=(10, 5))

axes[0].imshow(image, cmap="gray", interpolation="nearest", vmin=0, vmax=255)
axes[0].set_title("Original aerial image")
axes[0].axis("off")

axes[1].imshow(equalized_image, cmap="gray", interpolation="nearest", vmin=0, vmax=255)
axes[1].set_title("Histogram equalized")
axes[1].axis("off")

plt.savefig("results/aerial_equalization_comparison.png", dpi=150, bbox_inches="tight")

intensities = np.arange(256)

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

axes[0].bar(intensities, histogram, width=1.0, color="gray")
axes[0].set_title("Original histogram")
axes[0].set_xlabel("Intensity")
axes[0].set_ylabel("Number of pixels")
axes[0].set_xlim(0, 255)

axes[1].bar(intensities, equalized_hist, width=1.0, color="gray")
axes[1].set_title("Equalized histogram")
axes[1].set_xlabel("Intensity")
axes[1].set_ylabel("Number of pixels")
axes[1].set_xlim(0, 255)

plt.tight_layout()
plt.savefig("results/aerial_equalization_histograms.png", dpi=150, bbox_inches="tight")

plt.show()