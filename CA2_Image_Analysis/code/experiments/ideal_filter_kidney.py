import numpy as np
from matplotlib import pyplot as plt
from libtiff import TIFF

from frequency_filters import ideal_low_pass, ideal_high_pass


def apply_frequency_filter(image, mask):
    spectrum = np.fft.fftshift(np.fft.fft2(image))
    filtered_spectrum = spectrum * mask
    reconstructed = np.fft.ifft2(
        np.fft.ifftshift(filtered_spectrum)
    )
    return reconstructed.real


def main():
    image_path = "data/raw/ImgSetCa2/Kidney1-Crop.tif"

    tif = TIFF.open(image_path, mode="r")
    image = tif.read_image().astype(float)
    tif.close()

    cutoff = 30

    low_mask = ideal_low_pass(image.shape, cutoff)
    high_mask = ideal_high_pass(image.shape, cutoff)

    low_image = apply_frequency_filter(image, low_mask)
    high_image = apply_frequency_filter(image, high_mask)

    # Two filtered components reconstruct

    reconstruction_error = np.max(
        np.abs(image - (low_image + high_image))
    )

    print("Image dimensions:", image.shape)
    print("Cutoff radius:", cutoff)
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
    axes[1].set_title("Ideal low-pass (D0 = 30)")

    # High-pass output is signed and approximately zero-mean.
    # Display it around middle gray to reveal positive
    # and negative edge responses.
    high_display = high_image + 128

    axes[2].imshow(
        high_display, cmap="gray", vmin=0, vmax=255
    )
    axes[2].set_title("Ideal high-pass (offset +128)")

    for axis in axes:
        axis.axis("off")

    plt.tight_layout()
    plt.savefig(
        "results/figures/ideal_filter_kidney.png",
        dpi=200,
        bbox_inches="tight"
    )
    plt.close(fig)

    print("Figure saved successfully.")


if __name__ == "__main__":
    main()