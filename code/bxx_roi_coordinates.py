from libtiff import TIFF
from matplotlib import pyplot as plt
import numpy as np

tiff_file = TIFF.open("data/BXX/BXX/BXX_GLOM.tif", mode="r")
glom = tiff_file.read_image()

print("Mask shape:", glom.shape)
print("Mask data type:", glom.dtype)

values, counts = np.unique(glom, return_counts=True)
for v, c in zip(values, counts):
    print(f"  value {v}: {c} pixels")

mask = glom == 3

plt.figure(figsize=(5, 10))
plt.imshow(mask, cmap="gray", interpolation="nearest")
plt.title("All segmented glomeruli")
plt.xlabel("Column")
plt.ylabel("Row")
plt.savefig("results/bxx_all_glomeruli.png", dpi=150, bbox_inches="tight")

boxes = {
    3: (4398, 4563, 434, 586),
    4: (3779, 3996, 732, 950),
    5: (3473, 3660, 698, 880),
}

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

for ax, (number, (r0, r1, c0, c1)) in zip(axes, boxes.items()):
    region = mask[r0:r1, c0:c1]
    n_pixels = np.count_nonzero(region)
    fraction = n_pixels / region.size

    print(f"\nGlomerulus {number}")
    print("  Region shape:", region.shape)
    print("  Foreground pixels:", n_pixels)
    print(f"  Fraction of box covered: {fraction:.2%}")

    ax.imshow(region, cmap="gray", interpolation="nearest")
    ax.set_title(f"Glomerulus {number} segmentation region")
    ax.axis("off")

plt.tight_layout()
plt.savefig("results/bxx_glom345_regions.png", dpi=150, bbox_inches="tight")
plt.show()