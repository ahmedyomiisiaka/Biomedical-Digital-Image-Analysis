import numpy as np
from matplotlib import pyplot as plt
from libtiff import TIFF

from spatial_frequency_comparison import spatial_average


def gaussian_kernel(sigma=2.0, radius=6):
    coordinates = np.arange(-radius, radius + 1)
    rows, cols = np.meshgrid(coordinates, coordinates, indexing="ij")

    kernel = np.exp(-(rows**2 + cols**2) / (2 * sigma**2))
    return kernel / kernel.sum()


def spatial_gaussian(image, kernel):
    height, width = image.shape
    radius = kernel.shape[0] // 2

    result = np.zeros_like(image, dtype=float)

    for i in range(kernel.shape[0]):
        for j in range(kernel.shape[1]):
            dr = i - radius
            dc = j - radius

            result += kernel[i, j] * np.roll(
                image, shift=(dr, dc), axis=(0, 1)
            )

    return result


def frequency_gaussian(image, kernel):
    height, width = image.shape
    radius = kernel.shape[0] // 2

    padded_kernel = np.zeros((height, width), dtype=float)

    for i in range(kernel.shape[0]):
        for j in range(kernel.shape[1]):
            dr = i - radius
            dc = j - radius
            padded_kernel[dr % height, dc % width] = kernel[i, j]

    result = np.fft.ifft2(
        np.fft.fft2(image) * np.fft.fft2(padded_kernel)
    )

    return result.real


def main():
    tif = TIFF.open("data/raw/ImgSetCa2/Kidney1-Crop.tif", mode="r")
    image = tif.read_image().astype(float)
    tif.close()

    sigma = 2.0
    kernel = gaussian_kernel(sigma=sigma, radius=6)

    spatial = spatial_gaussian(image, kernel)
    frequency = frequency_gaussian(image, kernel)

    difference = np.abs(spatial - frequency)

    print("Kernel sum:", kernel.sum())
    print("Image shape:", image.shape)
    print("Maximum absolute difference:", difference.max())
    print("Mean absolute difference:", difference.mean())

    assert np.isclose(kernel.sum(), 1.0)
    assert difference.max() < 1e-10

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    for ax, data, title in zip(
        axes,
        [image, spatial, frequency],
        ["Original", "Spatial Gaussian", "Frequency Gaussian"]
    ):
        ax.imshow(data, cmap="gray", vmin=0, vmax=255)
        ax.set_title(title)
        ax.axis("off")

    plt.tight_layout()
    plt.savefig(
        "results/figures/gaussian_spatial_frequency.png",
        dpi=200,
        bbox_inches="tight"
    )
    plt.close()

    print("Gaussian spatial-frequency comparison: PASS")


if __name__ == "__main__":
    main()