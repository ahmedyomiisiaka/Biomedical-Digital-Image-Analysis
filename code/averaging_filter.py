from libtiff import TIFF
from matplotlib import pyplot as plt
import numpy as np

tiff_file = TIFF.open("data/ImgSet3/imgset3/Fig0333(a)(test_pattern_blurring_orig).tif", mode="r")
image = tiff_file.read_image()

height, width = image.shape
image_float = image.astype(np.float64)
blurred = image_float.copy()

for row in range(1, height - 1):
    for col in range(1, width - 1):
        neighborhood = image_float[row - 1:row + 2, col - 1:col + 2]
        blurred[row, col] = np.mean(neighborhood)

print("Blurred image shape:", blurred.shape)
print("Blurred minimum:", np.min(blurred))
print("Blurred maximum:", np.max(blurred))
print("Blurred mean:", np.mean(blurred))

fig, axes = plt.subplots(1, 2, figsize=(10, 5))

axes[0].imshow(image, cmap="gray", interpolation="nearest", vmin=0, vmax=255)
axes[0].set_title("Original")
axes[0].axis("off")

axes[1].imshow(blurred, cmap="gray", interpolation="nearest", vmin=0, vmax=255)
axes[1].set_title("3 x 3 average (unchanged border)")
axes[1].axis("off")

plt.savefig("results/averaging_filter_3x3.png", dpi=150, bbox_inches="tight")
plt.show()