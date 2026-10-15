from libtiff import TIFF
from matplotlib import pyplot as plt

slide_file = TIFF.open("data/ImgSet1/imgset1/Kidney2_RGB2_20x.svs", mode="r")

slide_file.SetDirectory(0)

print("Is tiled:", slide_file.IsTiled())

x = 3840
y = 19200
tile = slide_file.read_one_tile(x, y)

print("Tile shape:", tile.shape)
print("Tile data type:", tile.dtype)
print("Minimum pixel value:", tile.min())
print("Maximum pixel value:", tile.max())

plt.imshow(tile, interpolation="nearest", vmin=0, vmax=255)
plt.title("Kidney WSI - tile at (3840, 19200)")
plt.axis("off")
plt.savefig("results/kidney_tissue_tile.png", dpi=150, bbox_inches="tight")
plt.show()