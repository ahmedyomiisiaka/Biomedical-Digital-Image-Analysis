from libtiff import TIFF
from matplotlib import pyplot as plt
import numpy as np

tiff_file = TIFF.open("data/ImgSet2/imgset2/Fig0309(a)(washed_out_aerial_image).tif", mode="r")
image = tiff_file.read_image()

low = 100
high = 220

stretched_image = np.zeros(image.shape, dtype=np.uint8)

height, width = image.shape

for row in range(height):
    for col in range(width):

        pixel = int(image[row, col])

        if pixel < low:
            new_intensity = 0
        elif pixel > high:
            new_intensity = 255
        else:
            new_intensity = 255 * (pixel - low) / (high - low)

        
        stretched_image[row, col] = int(round(new_intensity))

print("Original mean:", image.mean())
print("Stretched mean:", stretched_image.mean())
print("Original pixel (100,100):", image[100, 100])
print("Stretched pixel (100,100):", stretched_image[100, 100])
print("Output shape:", stretched_image.shape)

plt.imsave("results/aerial_contrast_stretched.png", stretched_image, cmap="gray", vmin=0, vmax=255)

fig, axes = plt.subplots(1, 2, figsize=(10, 5))

axes[0].imshow(image, cmap="gray", interpolation="nearest", vmin=0, vmax=255)
axes[0].set_title("Original")
axes[0].axis("off")

axes[1].imshow(stretched_image, cmap="gray", interpolation="nearest", vmin=0, vmax=255)
axes[1].set_title("Contrast stretched (100 to 220)")
axes[1].axis("off")

plt.savefig("results/aerial_contrast_comparison.png", dpi=150, bbox_inches="tight")

original_hist = np.bincount(image.ravel(), minlength=256)
stretched_hist = np.bincount(stretched_image.ravel(), minlength=256)

print("Original histogram total:", original_hist.sum())
print("Stretched histogram total:", stretched_hist.sum())
print("Pixels at intensity 0 after stretching:", stretched_hist[0])
print("Pixels at intensity 255 after stretching:", stretched_hist[255])

intensities = np.arange(256)

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

axes[0].bar(intensities, original_hist, width=1.0, color="gray")
axes[0].set_title("Original histogram")
axes[0].set_xlabel("Intensity")
axes[0].set_ylabel("Number of pixels")
axes[0].set_xlim(0, 255)

axes[1].bar(intensities, stretched_hist, width=1.0, color="gray")
axes[1].set_title("Stretched histogram")
axes[1].set_xlabel("Intensity")
axes[1].set_ylabel("Number of pixels")
axes[1].set_xlim(0, 255)

plt.tight_layout()
plt.savefig("results/aerial_contrast_histograms.png", dpi=150, bbox_inches="tight")

plt.show()