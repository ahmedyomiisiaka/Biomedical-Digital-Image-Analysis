from libtiff import TIFF
from matplotlib import pyplot as plt
import numpy as np


tiff_file = TIFF.open("data/ImgSet4/imgset4/Pattern64.tif", mode="r")
image = tiff_file.read_image()

scale = 2
height, width = image.shape
new_height = height * scale
new_width = width * scale

image_float = image.astype(np.float64)
bilinear = np.zeros((new_height, new_width), dtype=np.float64)

nearest = np.zeros((new_height, new_width), dtype=image.dtype)

for row in range(new_height):
    for col in range(new_width):
        source_y = row / scale
        source_x = col / scale

        y0 = int(np.floor(source_y))
        x0 = int(np.floor(source_x))
        y1 = min(y0 + 1, height - 1)
        x1 = min(x0 + 1, width - 1)

        dy = source_y - y0
        dx = source_x - x0

        top_left = image_float[y0, x0]
        top_right = image_float[y0, x1]
        bottom_left = image_float[y1, x0]
        bottom_right = image_float[y1, x1]

        top = (1 - dx) * top_left + dx * top_right
        bottom = (1 - dx) * bottom_left + dx * bottom_right
        bilinear[row, col] = (1 - dy) * top + dy * bottom

        nearest[row, col] = image[row // scale, col // scale]

bilinear_uint8 = np.clip(np.round(bilinear), 0, 255).astype(np.uint8)

print("Original shape:", image.shape)
print("Bilinear shape:", bilinear.shape)
print("Bilinear data type (computed):", bilinear.dtype)
print("Bilinear data type (displayed):", bilinear_uint8.dtype)
print("Original pixel (0,0):", image[0, 0])
print("Bilinear pixel (0,0):", bilinear[0, 0])
print("Bilinear pixel (1,1):", bilinear[1, 1])
print("Bilinear minimum:", np.min(bilinear))
print("Bilinear maximum:", np.max(bilinear))
print("Displayed minimum:", np.min(bilinear_uint8))
print("Displayed maximum:", np.max(bilinear_uint8))

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

axes[0].imshow(image, cmap="gray", interpolation="nearest", vmin=0, vmax=255)
axes[0].set_title("Original (64 x 64)")

axes[1].imshow(nearest, cmap="gray", interpolation="nearest", vmin=0, vmax=255)
axes[1].set_title("Nearest-neighbor (128 x 128)")

axes[2].imshow(bilinear_uint8, cmap="gray", interpolation="nearest", vmin=0, vmax=255)
axes[2].set_title("Bilinear (128 x 128)")

plt.tight_layout()
plt.savefig("results/pattern_interpolation_comparison.png", dpi=150, bbox_inches="tight")
plt.show()