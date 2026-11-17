import numpy as np
from matplotlib import pyplot as plt
from libtiff import TIFF

from frequency_filters import (
    butterworth_low_pass,
    butterworth_high_pass
)

from ideal_filter_kidney import apply_frequency_filter


def main():
    image_path = "data/raw/ImgSetCa2/Kidney1-Crop.tif"

    tif = TIFF.open(image_path, mode="r")
    image = tif.read_image().astype(float)
    tif.close()

    cutoff = 30
    orders = [1, 2, 4]

    fig, axes = plt.subplots(2, 4, figsize=(16, 9))

    axes[0, 0].imshow(image, cmap="gray", vmin=0, vmax=255)
    axes[0, 0].set_title("Original image")

    axes[1, 0].imshow(image, cmap="gray", vmin=0, vmax=255)
    axes[1, 0].set_title("Original image")

    for column, order in enumerate(orders, start=1):
        low_mask = butterworth_low_pass(
            image.shape, cutoff, order
        )
        high_mask = butterworth_high_pass(
            image.shape, cutoff, order
        )

        low_image = apply_frequency_filter(image, low_mask)
        high_image = apply_frequency_filter(image, high_mask)

        error = np.max(
            np.abs(image - (low_image + high_image))
        )

        assert error < 1e-8

        print(
            f"Order {order}: reconstruction error = {error:.6e}"
        )

        axes[0, column].imshow(
            low_image, cmap="gray", vmin=0, vmax=255
        )
        axes[0, column].set_title(
            f"Butterworth LP, n={order}"
        )

        axes[1, column].imshow(
            high_image + 128,
            cmap="gray", vmin=0, vmax=255
        )
        axes[1, column].set_title(
            f"Butterworth HP, n={order}"
        )

    for axis in axes.flat:
        axis.axis("off")

    plt.suptitle(
        "Butterworth Filtering: Cutoff Radius = 30",
        fontsize=15
    )

    plt.tight_layout()

    plt.savefig(
        "results/figures/butterworth_kidney.png",
        dpi=200,
        bbox_inches="tight"
    )

    plt.close(fig)

    print("Butterworth comparison figure saved.")


if __name__ == "__main__":
    main()