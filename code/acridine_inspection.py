from libtiff import TIFF
from matplotlib import pyplot as plt

tiff_file = TIFF.open("data/ImgSet1/imgset1/Region_001_FOV_00041_Acridine_Or_Gray.tif", mode="r")
acridine_image = tiff_file.read_image()
print("Image shape:", acridine_image.shape)
print("Image data type:", acridine_image.dtype)
print("Minimum pixel value:", acridine_image.min())
print("Maximum pixel value:", acridine_image.max())

plt.imshow(acridine_image, cmap="gray", interpolation="nearest", vmin=0, vmax=255)
plt.title("Acridine Orange fluorescence - grayscale")
plt.axis("off")
plt.savefig("results/acridine_grayscale.png", dpi=150, bbox_inches="tight")
plt.show()