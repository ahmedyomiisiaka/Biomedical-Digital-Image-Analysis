import os

import numpy as np
from libtiff import TIFF
from matplotlib import pyplot as plt


def spatial_difference(image):
    return np.roll(image, -1, axis=1) - image


def frequency_difference(image):
    height, width = image.shape

    frequencies = np.arange(width)

    response = np.exp(
        2j * np.pi * frequencies / width
    ) - 1

    spectrum = np.fft.fft2(image)

    result = np.fft.ifft2(
        spectrum * response[np.newaxis, :]
    )

    return result.real


def main():
    tif = TIFF.open(
        "data/raw/ImgSetCa2/Kidney1-Crop.tif", mode="r"
    )
    image = tif.read_image().astype(float)
    tif.close()

    spatial = spatial_difference(image)
    frequency = frequency_difference(image)

    error = np.max(np.abs(spatial - frequency))

    print("Image shape:", image.shape)
    print("Maximum absolute difference:", error)

    assert error < 1e-10

    print("Differentiation equivalence: PASS")

    fig, axes = plt.subplots(1, 4, figsize=(16, 5))

    images = [
        image,
        spatial,
        frequency,
        np.abs(spatial - frequency)
    ]

    titles = [
        "Original kidney",
        "Spatial horizontal difference",
        "Frequency horizontal difference",
        "Absolute difference"
    ]

    for index, ax in enumerate(axes):

        if index == 0:
            ax.imshow(images[index], cmap="gray",
                      vmin=0, vmax=255)
        elif index == 3:
            ax.imshow(images[index], cmap="gray",
                      vmin=0, vmax=1e-10)
        else:
            ax.imshow(images[index], cmap="gray",
                      vmin=-128, vmax=128)

        ax.set_title(titles[index])
        ax.axis("off")

    plt.tight_layout()

    os.makedirs("results/figures", exist_ok=True)

    plt.savefig(
        "results/figures/differentiation_comparison.png",
        dpi=200,
        bbox_inches="tight"
    )
    plt.close(fig)

    print("Figure saved: results/figures/differentiation_comparison.png")


if __name__ == "__main__":
    main()