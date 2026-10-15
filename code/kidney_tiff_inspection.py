from libtiff import TIFF
from matplotlib import pyplot as plt

tiff_file = TIFF.open("data/ImgSet1/imgset1/Kidney1.tif", mode="r")
kidney_image = tiff_file.read_image()
print("Image shape:", kidney_image.shape)
print("Image data type:", kidney_image.dtype)
print("Minimum pixel value:", kidney_image.min())
print("Maximum pixel value:", kidney_image.max())

plt.imshow(kidney_image, interpolation="nearest", vmin=0, vmax=255)
plt.title("Kidney tissue - original RGB image")
plt.axis("off")
plt.savefig("results/kidney_original_rgb.png", dpi=150, bbox_inches="tight")
plt.show()