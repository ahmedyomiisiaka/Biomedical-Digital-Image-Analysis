import numpy as np
from matplotlib import pyplot as plt
from libtiff import TIFF

from frequency_filters import ideal_band_pass, ideal_band_stop
from ideal_filter_kidney import apply_frequency_filter


def main():
    path = "data/raw/ImgSetCa2/Kidney1-Crop.tif"

    tif = TIFF.open(path, mode="r")
    image = tif.read_image().astype(float)
    tif.close()

    inner_cutoff = 15
    outer_cutoff = 60

    pass_mask = ideal_band_pass(
        image.shape, inner_cutoff, outer_cutoff
    )
    stop_mask = ideal_band_stop(
        image.shape, inner_cutoff, outer_cutoff
    )

    passed = apply_frequency_filter(image, pass_mask)
    stopped = apply_frequency_filter(image, stop_mask)

    error = np.max(np.abs(image - (passed + stopped)))

    print("Image shape:", image.shape)
    print("Band-pass range:", passed.min(), passed.max())
    print("Band-stop range:", stopped.min(), stopped.max())
    print("Reconstruction error:", error)

    assert error < 1e-8

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    axes[0].imshow(image, cmap="gray", vmin=0, vmax=255)
    axes[0].set_title("Original kidney")

    # Band-pass output is signed; offset for visualization.
    axes[1].imshow(
        passed + 128, cmap="gray", vmin=0, vmax=255
    )
    axes[1].set_title("Ideal band-pass (15–60), offset +128")

    axes[2].imshow(
        stopped, cmap="gray", vmin=0, vmax=255
    )
    axes[2].set_title("Ideal band-stop (15–60)")

    for axis in axes:
        axis.axis("off")

    plt.tight_layout()
    plt.savefig(
        "results/figures/band_filter_kidney.png",
        dpi=200,
        bbox_inches="tight"
    )
    plt.close()

    print("Band-filter comparison: PASS")
    print("Figure saved: results/figures/band_filter_kidney.png")


if __name__ == "__main__":
    main()