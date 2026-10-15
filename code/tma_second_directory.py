from libtiff import TIFF
from matplotlib import pyplot as plt

tiff_file = TIFF.open("data/ImgSet1/imgset1/TMA2-v2.tif", mode="r")
tiff_file.SetDirectory(1)
tma_image = tiff_file.read_image()
print("Image shape:", tma_image.shape)
print("Image data type:", tma_image.dtype)
print("Minimum pixel value:", tma_image.min())
print("Maximum pixel value:", tma_image.max())

plt.imshow(tma_image, interpolation="nearest", vmin=0, vmax=255)
plt.title("TMA2 - second TIFF directory")
plt.axis("off")
plt.savefig("results/tma_directory1.png", dpi=150, bbox_inches="tight")
plt.show()