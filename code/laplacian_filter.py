from libtiff import TIFF
from matplotlib import pyplot as plt
import numpy as np

tiff_file = TIFF.open("data/ImgSet3/imgset3/Fig0333(a)(test_pattern_blurring_orig).tif", mode="r")
image = tiff_file.read_image()

image_float = image.astype(np.float64)
height, width = image.shape
laplacian = np.zeros(image.shape, dtype=np.float64)

for row in range(1, height - 1):
    for col in range(1, width - 1):
        up = image_float[row - 1, col]
        down = image_float[row + 1, col]
        left = image_float[row, col - 1]
        right = image_float[row, col + 1]
        center = image_float[row, col]

        laplacian[row, col] = up + down + left + right - 4 * center

print("Laplacian shape:", laplacian.shape)
print("Laplacian minimum:", np.min(laplacian))
print("Laplacian maximum:", np.max(laplacian))
print("Laplacian mean:", np.mean(laplacian))

fig, axes = plt.subplots(1, 2, figsize=(10, 5))

axes[0].imshow(image, cmap="gray", interpolation="nearest", vmin=0, vmax=255)
axes[0].set_title("Original")
axes[0].axis("off")


axes[1].imshow(laplacian, cmap="gray", interpolation="nearest", vmin=-1020, vmax=1020)
axes[1].set_title("Laplacian")
axes[1].axis("off")

plt.tight_layout()
plt.savefig("results/laplacian_comparison.png", dpi=150, bbox_inches="tight")
plt.show()