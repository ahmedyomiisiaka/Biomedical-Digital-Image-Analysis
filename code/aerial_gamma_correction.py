from libtiff import TIFF
from matplotlib import pyplot as plt
import numpy as np

tiff_file = TIFF.open("data/ImgSet2/imgset2/Fig0309(a)(washed_out_aerial_image).tif", mode="r")
image = tiff_file.read_image()

gamma = 2.0

corrected_float = 255 * (image / 255) ** gamma

corrected_image = np.round(corrected_float).astype(np.uint8)
print("Original  - min:", image.min(), "max:", image.max())
print("Corrected - min:", corrected_image.min(), "max:", corrected_image.max())
print("Corrected shape:", corrected_image.shape)
print("Corrected data type:", corrected_image.dtype)

print("Original pixel at (100, 100):", image[100, 100])
print("Corrected pixel at (100, 100):", corrected_image[100, 100])
print("Original mean intensity:", image.mean())
print("Corrected mean intensity:", corrected_image.mean())

plt.imsave("results/aerial_gamma_20.png", corrected_image, cmap="gray", vmin=0, vmax=255)

fig, axes = plt.subplots(1, 2, figsize=(10, 5))

axes[0].imshow(image, cmap="gray", interpolation="nearest", vmin=0, vmax=255)
axes[0].set_title("Original")
axes[0].axis("off")

axes[1].imshow(corrected_image, cmap="gray", interpolation="nearest", vmin=0, vmax=255)
axes[1].set_title("Gamma corrected (gamma = 2.0)")
axes[1].axis("off")

plt.savefig("results/aerial_gamma_20_comparison.png", dpi=150, bbox_inches="tight")
plt.show()