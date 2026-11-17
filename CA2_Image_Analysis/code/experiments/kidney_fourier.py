import numpy as np
import matplotlib.pyplot as plt
from libtiff import TIFF

from fourier_transform import (
    zero_pad_image,
    shift_periodicity,
    forward_fourier,
    inverse_fourier,
    crop_image,
)


def load_tiff(filename):
    """Load a grayscale TIFF image."""
    tif = TIFF.open(filename, mode="r")

    try:
        image = tif.read_image()
    finally:
        tif.close()

    if image.ndim != 2:
        raise ValueError("Expected a two-dimensional grayscale image")

    return image


def run_pipeline(image):
    """Perform the six Fourier processing stages."""

    padded = zero_pad_image(image)
    shifted = shift_periodicity(padded)
    spectrum = forward_fourier(shifted)

    inverse = inverse_fourier(spectrum)

    # Reverse the periodicity shift after inverse FFT.
    unshifted = shift_periodicity(inverse.real)

    # Recover the original image dimensions.
    reconstructed = crop_image(unshifted, image.shape)

    return padded, shifted, spectrum, inverse, unshifted, reconstructed


def report_errors(original, inverse, reconstructed):
    """Measure numerical reconstruction accuracy."""

    error = np.abs(
        original.astype(np.float64) - reconstructed
    )

    max_imaginary = np.max(np.abs(inverse.imag))
    max_error = np.max(error)
    mean_error = np.mean(error)

    correct = np.allclose(
        original,
        reconstructed,
        atol=1e-10,
        rtol=0
    )

    print("Maximum imaginary residual:", max_imaginary)
    print("Maximum reconstruction error:", max_error)
    print("Mean absolute error:", mean_error)
    print("Reconstruction correct:", correct)

    assert max_imaginary < 1e-10
    assert correct


def save_figure(original, padded, shifted,
                spectrum, unshifted, reconstructed):
    """Save the six stages specified in CA2 Section 1.1."""

    stages = [
        ("a. Original kidney image", original),
        ("b. Zero-padded image", padded),
        ("c. Periodicity-shifted image", shifted),
        ("d. Centered Fourier log-magnitude",
         np.log1p(np.abs(spectrum))),
        ("e. Inverse FFT with shift reversed", unshifted),
        ("f. Cropped reconstruction", reconstructed),
    ]

    fig, axes = plt.subplots(2, 3, figsize=(15, 10))

    for index, (ax, (title, data)) in enumerate(
        zip(axes.ravel(), stages)
    ):

        if index in (0, 1, 4, 5):
            ax.imshow(
                data,
                cmap="gray",
                interpolation="nearest",
                vmin=0,
                vmax=255
            )

        elif index == 2:
            ax.imshow(
                data,
                cmap="gray",
                interpolation="nearest",
                vmin=-255,
                vmax=255
            )

        else:
            ax.imshow(
                data,
                cmap="gray",
                interpolation="nearest"
            )

        ax.set_title(
            f"{title}\n"
            f"{data.shape[1]} × {data.shape[0]} pixels"
        )

        ax.axis("off")

    fig.tight_layout()

    output = "results/figures/kidney_six_stages.png"

    fig.savefig(output, dpi=200)
    plt.close(fig)

    print("Saved figure:", output)


def test_reconstruction(name, image):
    """Run the same reconstruction validation on different images."""

    padded, shifted, spectrum, inverse, unshifted, reconstructed = (
        run_pipeline(image)
    )

    print("\n---", name, "---")
    print("Original shape:", image.shape)
    print("Padded shape:", padded.shape)
    print("Reconstructed shape:", reconstructed.shape)

    report_errors(image, inverse, reconstructed)

    return padded, shifted, spectrum, unshifted, reconstructed


if __name__ == "__main__":

    filename = "data/raw/ImgSetCa2/Kidney1-Crop.tif"

    kidney = load_tiff(filename)

    padded, shifted, spectrum, unshifted, reconstructed = (
        test_reconstruction("Kidney image", kidney)
    )

    save_figure(
        kidney,
        padded,
        shifted,
        spectrum,
        unshifted,
        reconstructed
    )

    # Test 2: Non-square image
    rng = np.random.default_rng(0)

    rectangular = rng.integers(
        0, 256,
        size=(300, 500),
        dtype=np.uint8
    )

    test_reconstruction("Non-square image", rectangular)

    # Test 3: Constant image
    constant = np.full(
        (64, 96),
        128,
        dtype=np.uint8
    )

    test_reconstruction("Constant image", constant)

    # Test 4: Single bright pixel
    impulse = np.zeros(
        (64, 96),
        dtype=np.uint8
    )

    impulse[20, 30] = 255

    test_reconstruction("Single bright pixel", impulse)

    print("\nAll reconstruction tests passed.")