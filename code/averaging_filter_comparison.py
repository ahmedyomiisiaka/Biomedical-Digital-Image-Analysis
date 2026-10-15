from libtiff import TIFF
from matplotlib import pyplot as plt
import numpy as np

tiff_file = TIFF.open("data/ImgSet3/imgset3/Fig0333(a)(test_pattern_blurring_orig).tif", mode="r")
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

blurred_3 = average_filter(image, 3)
blurred_5 = average_filter(image, 5)
blurred_9 = average_filter(image, 9)

print("Original mean:", np.mean(image))
print("3 x 3 mean:", np.mean(blurred_3))
print("5 x 5 mean:", np.mean(blurred_5))
print("9 x 9 mean:", np.mean(blurred_9))

fig, axes = plt.subplots(2, 2, figsize=(10, 10))

axes[0, 0].imshow(image, cmap="gray", interpolation="nearest", vmin=0, vmax=255)
axes[0, 0].set_title("Original")
axes[0, 0].axis("off")

axes[0, 1].imshow(blurred_3, cmap="gray", interpolation="nearest", vmin=0, vmax=255)
axes[0, 1].set_title("3 x 3 average")
axes[0, 1].axis("off")

axes[1, 0].imshow(blurred_5, cmap="gray", interpolation="nearest", vmin=0, vmax=255)
axes[1, 0].set_title("5 x 5 average")
axes[1, 0].axis("off")

axes[1, 1].imshow(blurred_9, cmap="gray", interpolation="nearest", vmin=0, vmax=255)
axes[1, 1].set_title("9 x 9 average")
axes[1, 1].axis("off")

plt.tight_layout()
plt.savefig("results/averaging_filter_comparison.png", dpi=150, bbox_inches="tight")
plt.show()