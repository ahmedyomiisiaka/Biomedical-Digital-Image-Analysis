
import numpy as np
from matplotlib import pyplot as plt


# ---------------------------------------------------------
# Section 1.2: Fourier transforms of generated images
# ---------------------------------------------------------

HEIGHT = 256
WIDTH = 256
BACKGROUND = 128.0
AMPLITUDE = 100.0

OUTPUT_DIRECTORY = "results/figures"


def generate_cosine_image(shape, background, amplitude,
                          row_frequency, column_frequency):
    """Generate a 2D cosine image with specified frequencies."""

    height, width = shape

    if height <= 0 or width <= 0:
        raise ValueError("Image dimensions must be positive")

    if not all(
        isinstance(f, (int, np.integer))
        for f in (row_frequency, column_frequency)
    ):
        raise TypeError("Frequencies must be integers")

    if row_frequency < 0 or column_frequency < 0:
        raise ValueError("Frequencies must be non-negative")

    if row_frequency >= height // 2:
        raise ValueError("Row frequency must be below Nyquist")

    if column_frequency >= width // 2:
        raise ValueError("Column frequency must be below Nyquist")

    if amplitude < 0:
        raise ValueError("Amplitude must be non-negative")

    rows, columns = np.indices(shape)

    phase = 2 * np.pi * (
        row_frequency * rows / height
        + column_frequency * columns / width
    )

    image = background + amplitude * np.cos(phase)

    return image


def calculate_spectrum(image):
    """Calculate the centred Fourier magnitude spectrum."""

    spectrum = np.fft.fft2(image)

    centered = np.fft.fftshift(spectrum)

    magnitude = np.abs(centered)

    return magnitude


def expected_peak_positions(shape, row_frequency,
                            column_frequency):
    """Predict the locations of DC and cosine peaks."""

    height, width = shape

    center_row = height // 2
    center_column = width // 2

    positions = [(center_row, center_column)]

    if row_frequency == 0 and column_frequency == 0:
        return positions

    positions.append((
        center_row - row_frequency,
        center_column - column_frequency
    ))

    positions.append((
        center_row + row_frequency,
        center_column + column_frequency
    ))

    return positions


def validate_spectrum(magnitude, positions,
                      background, amplitude):
    """Compare measured Fourier peaks with theory."""

    height, width = magnitude.shape
    pixel_count = height * width

    expected_values = [background * pixel_count]

    if len(positions) == 3:
        cosine_peak = amplitude * pixel_count / 2

        expected_values.extend([
            cosine_peak,
            cosine_peak
        ])

    residual = magnitude.copy()

    print("Predicted and measured peaks:")

    for position, expected in zip(
        positions, expected_values
    ):
        measured = magnitude[position]

        print(
            f"  Position {position}: "
            f"expected={expected:.6f}, "
            f"measured={measured:.6f}"
        )

        assert np.isclose(
            measured,
            abs(expected),
            atol=1e-7,
            rtol=0
        )

        residual[position] = 0.0

    largest_unexpected = np.max(residual)

    print(
        "Largest unexpected coefficient:",
        f"{largest_unexpected:.6e}"
    )

    assert largest_unexpected < 1e-7

    print("Fourier validation: PASS")

    return largest_unexpected


def save_comparison_figure(image, magnitude,
                           title, filename):
    """Save image, full spectrum and enlarged spectrum."""

    log_magnitude = np.log1p(magnitude)

    fig, axes = plt.subplots(
        1, 3,
        figsize=(14, 4)
    )

    axes[0].imshow(
        image,
        cmap="gray",
        interpolation="nearest",
        vmin=0,
        vmax=255
    )

    axes[0].set_title("(a) " + title)
    axes[0].set_xlabel("Column")
    axes[0].set_ylabel("Row")

    axes[1].imshow(
        log_magnitude,
        cmap="gray",
        interpolation="nearest",
        vmin=0,
        vmax=np.max(log_magnitude)
    )

    axes[1].set_title("(b) Full Fourier spectrum")
    axes[1].set_xlabel("Horizontal frequency index")
    axes[1].set_ylabel("Vertical frequency index")

    axes[2].imshow(
        log_magnitude,
        cmap="gray",
        interpolation="nearest",
        vmin=0,
        vmax=np.max(log_magnitude)
    )

    center_row = image.shape[0] // 2
    center_column = image.shape[1] // 2

    zoom_radius = 16

    axes[2].set_xlim(
        center_column - zoom_radius,
        center_column + zoom_radius
    )

    axes[2].set_ylim(
        center_row + zoom_radius,
        center_row - zoom_radius
    )

    axes[2].set_title("(c) Enlarged central spectrum")
    axes[2].set_xlabel("Horizontal frequency index")
    axes[2].set_ylabel("Vertical frequency index")

    plt.tight_layout()

    output_path = OUTPUT_DIRECTORY + "/" + filename

    plt.savefig(output_path, dpi=200)
    plt.close(fig)

    print("Saved figure:", output_path)


def run_experiment(name, row_frequency,
                   column_frequency, filename):
    """Run one complete synthetic Fourier experiment."""

    print("\n---", name, "---")

    image = generate_cosine_image(
        (HEIGHT, WIDTH),
        BACKGROUND,
        AMPLITUDE,
        row_frequency,
        column_frequency
    )

    print("Image shape:", image.shape)
    print("Minimum intensity:", np.min(image))
    print("Maximum intensity:", np.max(image))

    magnitude = calculate_spectrum(image)

    positions = expected_peak_positions(
        image.shape,
        row_frequency,
        column_frequency
    )

    validate_spectrum(
        magnitude,
        positions,
        BACKGROUND,
        AMPLITUDE
    )

    save_comparison_figure(
        image,
        magnitude,
        name,
        filename
    )


def run_constant_experiment():
    """Validate the spectrum of a constant-intensity image."""

    print("\n--- Constant image ---")

    image = np.full(
        (HEIGHT, WIDTH),
        BACKGROUND,
        dtype=np.float64
    )

    magnitude = calculate_spectrum(image)

    positions = [(HEIGHT // 2, WIDTH // 2)]

    validate_spectrum(
        magnitude,
        positions,
        BACKGROUND,
        0.0
    )

    save_comparison_figure(
        image,
        magnitude,
        "Constant image",
        "constant_fourier.png"
    )


def main():

    print("Section 1.2: Synthetic Fourier experiments")

    run_constant_experiment()

    run_experiment(
        "Vertical cosine stripes",
        0,
        8,
        "vertical_stripes_fourier.png"
    )

    run_experiment(
        "Horizontal cosine stripes",
        8,
        0,
        "horizontal_stripes_fourier.png"
    )

    run_experiment(
        "Diagonal cosine stripes",
        6,
        8,
        "diagonal_stripes_fourier.png"
    )

    print("\nAll Section 1.2 experiments passed.")


if __name__ == "__main__":
    main()
