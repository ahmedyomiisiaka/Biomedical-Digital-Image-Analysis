from libtiff import TIFF
from matplotlib import pyplot as plt
import numpy as np

slide_file = TIFF.open("data/ImgSet1/imgset1/Kidney2_RGB2_20x.svs", mode="r")
slide_file.SetDirectory(0)


tile_size = 240
n_rows = 3
n_cols = 3

x_start = 2160
y_start = 24960

region = np.zeros((n_rows * tile_size, n_cols * tile_size, 3), dtype=np.uint8)

for row in range(n_rows):
    for col in range(n_cols):
        x = x_start + col * tile_size
        y = y_start + row * tile_size

        tile = slide_file.read_one_tile(x, y)

        top = row * tile_size
        left = col * tile_size
        region[top:top + tile_size, left:left + tile_size, :] = tile

print("Region shape:", region.shape)
print("Region data type:", region.dtype)

plt.imshow(region, interpolation="nearest", vmin=0, vmax=255)
plt.title("Kidney WSI - 3 x 3 tile region")
plt.axis("off")
plt.savefig("results/kidney_tile_region.png", dpi=150, bbox_inches="tight")
plt.show()