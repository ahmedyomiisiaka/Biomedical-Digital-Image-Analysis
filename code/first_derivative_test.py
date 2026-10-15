from libtiff import TIFF
from matplotlib import pyplot as plt
import numpy as np


tiff_file = TIFF.open("data/ImgSet3/imgset3/Fig0333(a)(test_pattern_blurring_orig).tif", mode="r")
image = tiff_file.read_image()

image_float = image.astype(np.float64)

horizontal_difference = image_float[:, 1:] - image_float[:, :-1]

print("Original shape:", image.shape)
print("Horizontal difference shape:", horizontal_difference.shape)
print("Minimum difference:", np.min(horizontal_difference))
print("Maximum difference:", np.max(horizontal_difference))

vertical_difference = image_float[1:, :] - image_float[:-1, :]

print("Vertical difference shape:", vertical_difference.shape)
print("Vertical minimum:", np.min(vertical_difference))
print("Vertical maximum:", np.max(vertical_difference))

dx = np.zeros(image.shape, dtype=np.float64)
dy = np.zeros(image.shape, dtype=np.float64)

dx[:, :-1] = horizontal_difference
dy[:-1, :] = vertical_difference

gradient = np.sqrt(dx ** 2 + dy ** 2)

print("Gradient shape:", gradient.shape)
print("Gradient minimum:", np.min(gradient))
print("Gradient maximum:", np.max(gradient))
print("Gradient mean:", np.mean(gradient))

fig, axes = plt.subplots(2, 2, figsize=(10, 10))

axes[0, 0].imshow(image, cmap="gray", interpolation="nearest", vmin=0, vmax=255)
axes[0, 0].set_title("Original")
axes[0, 0].axis("off")

axes[0, 1].imshow(dx, cmap="gray", interpolation="nearest", vmin=-255, vmax=255)
axes[0, 1].set_title("Horizontal derivative")
axes[0, 1].axis("off")

axes[1, 0].imshow(dy, cmap="gray", interpolation="nearest", vmin=-255, vmax=255)
axes[1, 0].set_title("Vertical derivative")
axes[1, 0].axis("off")

axes[1, 1].imshow(gradient, cmap="gray", interpolation="nearest", vmin=0, vmax=361)
axes[1, 1].set_title("Gradient magnitude")
axes[1, 1].axis("off")

plt.tight_layout()
plt.savefig("results/first_derivative_comparison.png", dpi=150, bbox_inches="tight")
plt.show()