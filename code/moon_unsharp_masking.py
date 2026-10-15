from libtiff import TIFF
from matplotlib import pyplot as plt
import numpy as np


tiff_file = TIFF.open("data/ImgSet3/imgset3/Fig0338(a)(blurry_moon).tif", mode="r")
image = tiff_file.read_image()


def average_filter(image, kernel_size):
    height, width = image.shape
    radius = kernel_size // 2

    image_float = image.astype(np.float64)
    result = image_float.copy()

    for row in range(radius, height - radius):
        for col in range(radius, width - radius):
            neighborhood = image_float[row - radius:row + radius + 1,
                                       col - radius:col + radius + 1]
            result[row, col] = np.mean(neighborhood)

    return result


blurred_moon = average_filter(image, 5)

image_float = image.astype(np.float64)
mask = image_float - blurred_moon

k = 1.0
sharpened_float = image_float + k * mask
sharpened = np.clip(sharpened_float, 0, 255).astype(np.uint8)

print("Original shape:", image.shape)
print("Original mean:", np.mean(image))
print("Blurred mean:", np.mean(blurred_moon))
print("Mask minimum:", np.min(mask))
print("Mask maximum:", np.max(mask))
print("Mask mean:", np.mean(mask))
print("Sharpened mean:", np.mean(sharpened))
print("Sharpened minimum:", np.min(sharpened))
print("Sharpened maximum:", np.max(sharpened))

fig, axes = plt.subplots(2, 2, figsize=(10, 10))

axes[0, 0].imshow(image, cmap="gray", interpolation="nearest", vmin=0, vmax=255)
axes[0, 0].set_title("Original moon")
axes[0, 0].axis("off")

axes[0, 1].imshow(blurred_moon, cmap="gray", interpolation="nearest", vmin=0, vmax=255)
axes[0, 1].set_title("5 x 5 blurred moon")
axes[0, 1].axis("off")

axes[1, 0].imshow(mask, cmap="gray", interpolation="nearest", vmin=-255, vmax=255)
axes[1, 0].set_title("Unsharp mask")
axes[1, 0].axis("off")

axes[1, 1].imshow(sharpened, cmap="gray", interpolation="nearest", vmin=0, vmax=255)
axes[1, 1].set_title("Sharpened moon (k = 1.0)")
axes[1, 1].axis("off")

plt.tight_layout()
plt.savefig("results/moon_unsharp_masking.png", dpi=150, bbox_inches="tight")
plt.show()