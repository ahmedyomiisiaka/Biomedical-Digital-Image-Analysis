from libtiff import TIFF
from matplotlib import pyplot as plt
import numpy as np

tiff_file = TIFF.open("data/ImgSet3/imgset3/Fig0343(a)(skeleton_orig).tif", mode="r")
image = tiff_file.read_image()

height, width = image.shape
image_float = image.astype(np.float64)

print("Image shape:", image.shape)
print("Image data type:", image.dtype)
print("Image minimum:", np.min(image))
print("Image maximum:", np.max(image))

laplacian = np.zeros(image.shape, dtype=np.float64)

for row in range(1, height - 1):
    for col in range(1, width - 1):
        up = image_float[row - 1, col]
        down = image_float[row + 1, col]
        left = image_float[row, col - 1]
        right = image_float[row, col + 1]
        center = image_float[row, col]

        laplacian[row, col] = 4 * center - up - down - left - right

print("\nLaplacian shape:", laplacian.shape)
print("Laplacian minimum:", np.min(laplacian))
print("Laplacian maximum:", np.max(laplacian))
print("Laplacian mean:", np.mean(laplacian))

sharpened = image_float + laplacian

print("\nStage c minimum:", np.min(sharpened))
print("Stage c maximum:", np.max(sharpened))
print("Stage c mean:", np.mean(sharpened))

sobel_x = np.array([
    [-1, 0, 1],
    [-2, 0, 2],
    [-1, 0, 1]
])
sobel_y = np.array([
    [-1, -2, -1],
    [0, 0, 0],
    [1, 2, 1]
])

gradient = np.zeros(image.shape, dtype=np.float64)

for row in range(1, height - 1):
    for col in range(1, width - 1):
        neighborhood = image_float[row - 1:row + 2, col - 1:col + 2]
        gx = np.sum(neighborhood * sobel_x)
        gy = np.sum(neighborhood * sobel_y)
        gradient[row, col] = np.sqrt(gx**2 + gy**2)

smoothed_gradient = gradient.copy()

for row in range(1, height - 1):
    for col in range(1, width - 1):
        neighborhood = gradient[row - 1:row + 2, col - 1:col + 2]
        smoothed_gradient[row, col] = np.mean(neighborhood)

print("\nStage d gradient minimum:", np.min(gradient))
print("Stage d gradient maximum:", np.max(gradient))
print("Stage e smoothed gradient maximum:", np.max(smoothed_gradient))
print("Stage e shape:", smoothed_gradient.shape)

gradient_max = np.max(smoothed_gradient)
if gradient_max > 0:
    gradient_normalized = smoothed_gradient / gradient_max
else:
    gradient_normalized = np.zeros_like(smoothed_gradient)

mask = sharpened * gradient_normalized

print("\nStage f mask minimum:", np.min(mask))
print("Stage f mask maximum:", np.max(mask))
print("Stage f mask mean:", np.mean(mask))

enhanced = image_float + mask

print("\nStage g minimum:", np.min(enhanced))
print("Stage g maximum:", np.max(enhanced))
print("Stage g pixels below 0:", np.count_nonzero(enhanced < 0))
print("Stage g pixels above 255:", np.count_nonzero(enhanced > 255))

gamma = 0.5
enhanced_clipped = np.clip(enhanced, 0, 255)
gamma_corrected = 255 * (enhanced_clipped / 255) ** gamma

print("\nStage h minimum:", np.min(gamma_corrected))
print("Stage h maximum:", np.max(gamma_corrected))
print("Stage h mean:", np.mean(gamma_corrected))


def scale_to_uint8(array):
    low, high = array.min(), array.max()
    return np.round((array - low) / (high - low) * 255).astype(np.uint8)


laplacian_display = scale_to_uint8(laplacian)
sharpened_display = np.clip(np.round(sharpened), 0, 255).astype(np.uint8)
gradient_display = scale_to_uint8(gradient)
smoothed_display = scale_to_uint8(smoothed_gradient)
mask_display = scale_to_uint8(mask)
enhanced_display = np.clip(np.round(enhanced), 0, 255).astype(np.uint8)
gamma_display = np.clip(np.round(gamma_corrected), 0, 255).astype(np.uint8)

fig, axes = plt.subplots(2, 4, figsize=(16, 13))

panels = [
    (image, "a: Original"),
    (laplacian_display, "b: Laplacian (scaled for display)"),
    (sharpened_display, "c: a + b"),
    (gradient_display, "d: Sobel gradient (scaled for display)"),
    (smoothed_display, "e: Smoothed gradient (scaled for display)"),
    (mask_display, "f: Mask = c x e (scaled for display)"),
    (enhanced_display, "g: a + f"),
    (gamma_display, "h: Gamma correction (gamma = 0.5)"),
]

for ax, (picture, title) in zip(axes.flat, panels):
    ax.imshow(picture, cmap="gray", interpolation="nearest", vmin=0, vmax=255)
    ax.set_title(title)
    ax.axis("off")

plt.tight_layout()
plt.savefig("results/skeleton_multistep_comparison.png", dpi=150, bbox_inches="tight")
plt.show()