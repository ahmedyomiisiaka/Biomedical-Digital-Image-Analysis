import numpy as np
from matplotlib import pyplot as plt

from frequency_filters import (
    ideal_low_pass,
    butterworth_low_pass,
    gaussian_low_pass
)

from ideal_filter_kidney import apply_frequency_filter


def make_step_image(size=256):
    """Generate a grayscale image with a vertical step."""

    image = np.full((size, size), 50.0)

    image[:, size // 2:] = 200.0

    return image


def measure_overshoot(profile, low_value=50, high_value=200):
    """Measure intensity excursions beyond the original range."""

    undershoot = max(0.0, low_value - np.min(profile))
    overshoot = max(0.0, np.max(profile) - high_value)

    return undershoot, overshoot


def main():

    image = make_step_image()

    cutoff = 20

    filters = {
        "Ideal": ideal_low_pass(image.shape, cutoff),
        "Butterworth n=2": butterworth_low_pass(
            image.shape, cutoff, 2
        ),
        "Butterworth n=4": butterworth_low_pass(
            image.shape, cutoff, 4
        ),
        "Gaussian": gaussian_low_pass(image.shape, cutoff)
    }

    # The middle row crosses the vertical intensity boundary.
    middle_row = image.shape[0] // 2

    profiles = {
        "Original": image[middle_row, :]
    }

    results = {}

    for name, mask in filters.items():

        filtered = apply_frequency_filter(image, mask)

        profile = filtered[middle_row, :]

        profiles[name] = profile

        undershoot, overshoot = measure_overshoot(profile)

        results[name] = (undershoot, overshoot)

        print(
            f"{name}: undershoot={undershoot:.6f}, "
            f"overshoot={overshoot:.6f}"
        )

        assert np.all(np.isfinite(filtered))

    # Figure 1: Intensity profiles near the central edge.
    plt.figure(figsize=(11, 6))

    columns = np.arange(image.shape[1])

    for name, profile in profiles.items():
        plt.plot(columns, profile, label=name)

    plt.xlim(95, 160)
    plt.xlabel("Column position")
    plt.ylabel("Pixel intensity")
    plt.title("Ringing Around a Sharp Intensity Boundary")
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.savefig(
        "results/figures/ringing_profiles.png",
        dpi=200,
        bbox_inches="tight"
    )

    plt.close()

    # Figure 2: Quantitative overshoot and undershoot.
    names = list(results.keys())

    undershoots = [results[name][0] for name in names]
    overshoots = [results[name][1] for name in names]

    positions = np.arange(len(names))
    width = 0.35

    plt.figure(figsize=(10, 5))

    plt.bar(
        positions - width / 2,
        undershoots,
        width,
        label="Undershoot"
    )

    plt.bar(
        positions + width / 2,
        overshoots,
        width,
        label="Overshoot"
    )

    plt.xticks(positions, names)
    plt.ylabel("Intensity excursion")
    plt.title("Ringing Artifact Comparison")
    plt.legend()

    plt.savefig(
        "results/figures/ringing_measurements.png",
        dpi=200,
        bbox_inches="tight"
    )

    plt.close()

    print("Ringing experiment figures saved.")


if __name__ == "__main__":
    main()