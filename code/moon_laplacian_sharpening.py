from libtiff import TIFF
from matplotlib import pyplot as plt
import numpy as np

tiff_file = TIFF.open("data/ImgSet3/imgset3/Fig0338(a)(blurry_moon).tif", mode="r")
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

sharpened_float = image_float - laplacian
sharpened = np.clip(sharpened_float, 0, 255).astype(np.uint8)

print("Original shape:", image.shape)
print("Original mean:", np.mean(image))
print("Sharpened mean:", np.mean(sharpened))
print("Sharpened minimum:", np.min(sharpened))
print("Sharpened maximum:", np.max(sharpened))

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

axes[0].imshow(image, cmap="gray", interpolation="nearest", vmin=0, vmax=255)
axes[0].set_title("Original moon")
axes[0].axis("off")

axes[1].imshow(laplacian, cmap="gray", interpolation="nearest", vmin=-1020, vmax=1020)
axes[1].set_title("Laplacian response")
axes[1].axis("off")

axes[2].imshow(sharpened, cmap="gray", interpolation="nearest", vmin=0, vmax=255)
axes[2].set_title("Sharpened moon")
axes[2].axis("off")

plt.tight_layout()
plt.savefig("results/moon_laplacian_sharpening.png", dpi=150, bbox_inches="tight")
plt.show()