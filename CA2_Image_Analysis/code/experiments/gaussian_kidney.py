import numpy as np
from matplotlib import pyplot as plt
from libtiff import TIFF

from frequency_filters import (
    gaussian_low_pass,
    gaussian_high_pass
)

from ideal_filter_kidney import apply_frequency_filter


def main():

    image_path = "data/raw/ImgSetCa2/Kidney1-Crop.tif"

    tif = TIFF.open(image_path, mode="r")
    image = tif.read_image().astype(float)
    tif.close()

    cutoff = 30

    low_mask = gaussian_low_pass(image.shape, cutoff)
    high_mask = gaussian_high_pass(image.shape, cutoff)

    low_image = apply_frequency_filter(image, low_mask)
    high_image = apply_frequency_filter(image, high_mask)

    reconstruction_error = np.max(
        np.abs(image - (low_image + high_image))
    )

    print("Image dimensions:", image.shape)
    print("Gaussian cutoff:", cutoff)
    print("Low-pass range:", low_image.min(), low_image.max())
    print("High-pass range:", high_image.min(), high_image.max())
    print("Reconstruction error:", reconstruction_error)

    assert reconstruction_error < 1e-8

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    axes[0].imshow(
        image, cmap="gray", vmin=0, vmax=255
    )
    axes[0].set_title("Original kidney image")

    axes[1].imshow(
        low_image, cmap="gray", vmin=0, vmax=255
    )
    axes[1].set_title("Gaussian low-pass (D0 = 30)")

    # The high-pass image contains signed values.
    # Add 128 for visualization only.
    axes[2].imshow(
        high_image + 128,
        cmap="gray", vmin=0, vmax=255
    )
    axes[2].set_title("Gaussian high-pass (offset +128)")

    for axis in axes:
        axis.axis("off")

    plt.tight_layout()

    plt.savefig(
        "results/figures/gaussian_kidney.png",
        dpi=200,
        bbox_inches="tight"
    )

    plt.close(fig)

    print("Gaussian comparison figure saved.")


if __name__ == "__main__":
    main()