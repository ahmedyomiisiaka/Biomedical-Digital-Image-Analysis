from libtiff import TIFF
from matplotlib import pyplot as plt
import numpy as np

tiff_file = TIFF.open("data/BXX/BXX/BXX_GLOM.tif", mode="r")
glom = tiff_file.read_image()

glom_rows, glom_cols = np.where(glom == 3)
print("Total glomeruli pixels:", len(glom_rows))

if len(glom_rows) > 0:
    print("Minimum row:", np.min(glom_rows))
    print("Maximum row:", np.max(glom_rows))
    print("Minimum column:", np.min(glom_cols))
    print("Maximum column:", np.max(glom_cols))

plt.figure(figsize=(5, 10))
plt.imshow(glom == 3, cmap="gray", interpolation="nearest")
plt.title("All segmented glomeruli")
plt.xlabel("Column")
plt.ylabel("Row")
plt.savefig(
    "results/bxx_all_glomeruli.png",
    dpi=150,
    bbox_inches="tight"
)
plt.show()

regions = {
    3: (4398, 4563, 434, 586),
    4: (3779, 3996, 732, 950),
    5: (3473, 3660, 698, 880)
}

for number, coordinates in regions.items():
    row_start, row_end, col_start, col_end = coordinates

    region = glom[row_start:row_end, col_start:col_end]

    print("Glomerulus", number)
    print("Region shape:", region.shape)
    print("Labels:", np.unique(region))
    print("Glomerulus pixels:", np.count_nonzero(region == 3))
    print("Value 255 pixels:", np.count_nonzero(region == 255))
    print("Background pixels:", np.count_nonzero(region == 0))

    print()

region3 = glom[4398:4563, 434:586]
rows255, cols255 = np.where(region3 == 255)

print("Glomerulus 3 - value 255 positions:")
if len(rows255) > 0:
    print("Row range (inside the box):", rows255.min(), "to", rows255.max())
    print("Column range (inside the box):", cols255.min(), "to", cols255.max())
    print("Row range (full mask):", rows255.min() + 4398, "to", rows255.max() + 4398)
    print("Column range (full mask):", cols255.min() + 434, "to", cols255.max() + 434)
else:
    print("No 255 pixels found in this box")