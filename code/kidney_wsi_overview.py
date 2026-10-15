from libtiff import TIFF
from matplotlib import pyplot as plt

tiff_file = TIFF.open("data/ImgSet1/imgset1/Kidney2_RGB2_20x.svs", mode="r")
tiff_file.SetDirectory(1)
overview_image = tiff_file.read_image()
print("Image shape:", overview_image.shape)
print("Image data type:", overview_image.dtype)
print("Minimum pixel value:", overview_image.min())
print("Maximum pixel value:", overview_image.max())

plt.imshow(overview_image, interpolation="nearest", vmin=0, vmax=255)
plt.xticks(range(0, 156, 10))
plt.yticks(range(0, 768, 50))
plt.grid()
plt.title("Kidney whole-slide image - overview")
## plt.axis("off")
plt.savefig("results/kidney_wsi_overview_grid.png", dpi=150, bbox_inches="tight")
plt.show()