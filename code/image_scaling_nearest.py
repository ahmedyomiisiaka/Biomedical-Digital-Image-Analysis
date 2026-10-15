from libtiff import TIFF
from matplotlib import pyplot as plt
import numpy as np

tiff_file = TIFF.open("data/ImgSet4/imgset4/Pattern64.tif", mode="r")
image = tiff_file.read_image()

scale = 2
height, width = image.shape
new_height = height * scale
new_width = width * scale
scaled = np.zeros((new_height, new_width), dtype=image.dtype)

for row in range(new_height):
    for col in range(new_width):
        source_row = row // scale
        source_col = col // scale
        scaled[row, col] = image[source_row, source_col]

print("Original shape:", image.shape)
print("Scaled shape:", scaled.shape)
print("Original pixel (0,0):", image[0, 0])
print("Scaled pixel (0,0):", scaled[0, 0])
print("Scaled pixel (1,1):", scaled[1, 1])

fig, axes = plt.subplots(1, 2, figsize=(10, 5))

axes[0].imshow(image, cmap="gray", interpolation="nearest", vmin=0, vmax=255)
axes[0].set_title("Original (64 x 64)")

axes[1].imshow(scaled, cmap="gray", interpolation="nearest", vmin=0, vmax=255)
axes[1].set_title("Nearest-neighbor, scale 2 (128 x 128)")

plt.tight_layout()
plt.savefig("results/pattern_scaling_nearest.png", dpi=150, bbox_inches="tight")
plt.show()