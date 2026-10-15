from libtiff import TIFF
from matplotlib import pyplot as plt
import numpy as np

tiff_file = TIFF.open("data/ImgSet4/imgset4/Pattern64.tif", mode="r")
image = tiff_file.read_image()

height, width = image.shape
image_float = image.astype(np.float64)

angle = np.deg2rad(30)

scale_matrix = np.array([
    [1.5, 0, 0],
    [0, 1.5, 0],
    [0, 0, 1]
])

rotation_matrix = np.array([
    [np.cos(angle), -np.sin(angle), 0],
    [np.sin(angle), np.cos(angle), 0],
    [0, 0, 1]
])

translation_matrix = np.array([
    [1, 0, 10],
    [0, 1, 5],
    [0, 0, 1]
])

composite = translation_matrix @ rotation_matrix @ scale_matrix
inverse = np.linalg.inv(composite)

print("Composite matrix:")
print(np.round(composite, 4))
print("\nInverse matrix:")
print(np.round(inverse, 4))

expected = np.array([
    [1.2990, -0.7500, 10],
    [0.7500, 1.2990, 5],
    [0, 0, 1]
])
print("\nMatches the expected matrix:", np.allclose(composite, expected, atol=1e-3))
print("Composite times inverse is the identity:", np.allclose(composite @ inverse, np.eye(3)))

out_height = 128
out_width = 128
transformed = np.zeros((out_height, out_width), dtype=np.float64)

inside_count = 0

for row in range(out_height):
    for col in range(out_width):
        source = inverse @ np.array([col, row, 1.0])
        source_x = source[0]
        source_y = source[1]

        if source_x < 0 or source_x > width - 1 or source_y < 0 or source_y > height - 1:
            continue

        inside_count += 1

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
        transformed[row, col] = (1 - dy) * top + dy * bottom

transformed_uint8 = np.clip(np.round(transformed), 0, 255).astype(np.uint8)

print("\nOriginal shape:", image.shape)
print("Output shape:", transformed_uint8.shape)
print("Output data type:", transformed_uint8.dtype)
print("Output pixels that map inside the original:", inside_count, "of", out_height * out_width)
print("Output minimum:", np.min(transformed_uint8))
print("Output maximum:", np.max(transformed_uint8))

fig, axes = plt.subplots(1, 2, figsize=(10, 5))

axes[0].imshow(image, cmap="gray", interpolation="nearest", vmin=0, vmax=255)
axes[0].set_title("Original (64 x 64)")
axes[0].axis("off")

axes[1].imshow(transformed_uint8, cmap="gray", interpolation="nearest", vmin=0, vmax=255)
axes[1].set_title("Scale 1.5, rotate 30 deg, translate (10, 5)")
axes[1].axis("off")

plt.tight_layout()
plt.savefig("results/composite_affine_transformation.png", dpi=150, bbox_inches="tight")
plt.show()