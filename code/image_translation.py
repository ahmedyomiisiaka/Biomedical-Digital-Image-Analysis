from libtiff import TIFF
from matplotlib import pyplot as plt
import numpy as np

tiff_file = TIFF.open("data/ImgSet4/imgset4/Pattern64.tif", mode="r")
image = tiff_file.read_image()

height, width = image.shape[:2]
translated = np.zeros(image.shape, dtype=image.dtype)
shift_x = 10 
shift_y = 5

for row in range(height):
    for col in range(width):
        source_row = row - shift_y
        source_col = col - shift_x

        if 0 <= source_row < height and 0 <= source_col < width:
            translated[row, col] = image[source_row, source_col]

print("Original shape:", image.shape)
print("Translated shape:", translated.shape)
print("Original pixel (0, 0):", image[0, 0])
print("Translated pixel (5, 10):", translated[5, 10])
print("Translated pixel (0, 0):", translated[0, 0])

fig, axes = plt.subplots(1, 2, figsize=(10, 5))

axes[0].imshow(image, cmap="gray", interpolation="nearest", vmin=0, vmax=255)
axes[0].set_title("Original")
axes[0].axis("off")

axes[1].imshow(translated, cmap="gray", interpolation="nearest", vmin=0, vmax=255)
axes[1].set_title("Translated (10 right, 5 down)")
axes[1].axis("off")

plt.tight_layout()
plt.savefig("results/pattern_translation.png", dpi=150, bbox_inches="tight")
plt.show()