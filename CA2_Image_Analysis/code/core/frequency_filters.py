import numpy as np


def frequency_distance(shape):
    """Calculate distance from the centre of a 2D frequency array."""

    height, width = shape

    if height <= 0 or width <= 0:
        raise ValueError("Image dimensions must be positive")

    rows, columns = np.indices((height, width))

    center_row = height // 2
    center_column = width // 2

    distance = np.sqrt(
        (rows - center_row) ** 2
        + (columns - center_column) ** 2
    )

    return distance


def ideal_low_pass(shape, cutoff):
    """Create an ideal low-pass frequency filter."""

    if cutoff <= 0:
        raise ValueError("Cutoff must be positive")

    distance = frequency_distance(shape)

    return (distance <= cutoff).astype(float)


def ideal_high_pass(shape, cutoff):
    """Create an ideal high-pass frequency filter."""

    return 1.0 - ideal_low_pass(shape, cutoff)


def butterworth_low_pass(shape, cutoff, order):
    """Create a Butterworth low-pass frequency filter."""

    if cutoff <= 0:
        raise ValueError("Cutoff must be positive")

    if not isinstance(order, (int, np.integer)) or order < 1:
        raise ValueError("Order must be a positive integer")

    distance = frequency_distance(shape)

    return 1.0 / (1.0 + (distance / cutoff) ** (2 * order))


def butterworth_high_pass(shape, cutoff, order):
    """Create a Butterworth high-pass frequency filter."""

    return 1.0 - butterworth_low_pass(shape, cutoff, order)


def gaussian_low_pass(shape, cutoff):
    """Create a Gaussian low-pass frequency filter."""

    if cutoff <= 0:
        raise ValueError("Cutoff must be positive")

    distance = frequency_distance(shape)

    return np.exp(-(distance ** 2) / (2 * cutoff ** 2))


def gaussian_high_pass(shape, cutoff):
    """Create a Gaussian high-pass frequency filter."""

    return 1.0 - gaussian_low_pass(shape, cutoff)


def ideal_band_pass(shape, inner_cutoff, outer_cutoff):
    """Retain frequencies between two radii."""

    if inner_cutoff < 0 or outer_cutoff <= inner_cutoff:
        raise ValueError("Invalid band limits")

    distance = frequency_distance(shape)

    return (
        (distance >= inner_cutoff)
        & (distance <= outer_cutoff)
    ).astype(float)


def ideal_band_stop(shape, inner_cutoff, outer_cutoff):
    """Suppress frequencies between two radii."""

    return 1.0 - ideal_band_pass(
        shape, inner_cutoff, outer_cutoff
    )


def ideal_notch_reject(shape, frequency_offsets, radius):
    """Reject circular regions around selected frequency offsets."""

    if radius <= 0:
        raise ValueError("Notch radius must be positive")

    rows, cols = np.indices(shape)

    centre_row = shape[0] // 2
    centre_col = shape[1] // 2

    mask = np.ones(shape, dtype=float)

    for row_offset, col_offset in frequency_offsets:

        distance = np.sqrt(
            (rows - (centre_row + row_offset)) ** 2
            + (cols - (centre_col + col_offset)) ** 2
        )

        mask[distance <= radius] = 0.0

    return mask


if __name__ == "__main__":

    distance = frequency_distance((256, 256))

    print("Distance array shape:", distance.shape)
    print("Distance at centre:", distance[128, 128])
    print("Distance one pixel from centre:", distance[128, 129])
    print("Distance ten pixels from centre:", distance[128, 138])

    assert distance.shape == (256, 256)
    assert distance[128, 128] == 0
    assert distance[128, 129] == 1
    assert distance[128, 138] == 10

    print("Frequency distance tests: PASS")

    print("\n--- Ideal filter tests ---")

    cutoff = 20

    low_pass = ideal_low_pass((256, 256), cutoff)
    high_pass = ideal_high_pass((256, 256), cutoff)

    assert low_pass.shape == (256, 256)
    assert high_pass.shape == (256, 256)

    # Low-pass retains the central frequency.
    assert low_pass[128, 128] == 1.0

    # High-pass removes the central frequency.
    assert high_pass[128, 128] == 0.0

    # Frequencies inside the cutoff.
    assert low_pass[128, 138] == 1.0
    assert high_pass[128, 138] == 0.0

    # Frequencies outside the cutoff.
    assert low_pass[128, 158] == 0.0
    assert high_pass[128, 158] == 1.0

    # The two filters must be complementary.
    assert np.allclose(low_pass + high_pass, 1.0)

    print("Ideal low-pass filter: PASS")
    print("Ideal high-pass filter: PASS")
    print("Filter complementarity: PASS")

    print("\n--- Butterworth filter tests ---")

    cutoff = 30
    order = 2

    low = butterworth_low_pass((256, 256), cutoff, order)
    high = butterworth_high_pass((256, 256), cutoff, order)

    assert low.shape == (256, 256)
    assert high.shape == (256, 256)

    assert np.isclose(low[128, 128], 1.0)
    assert np.isclose(high[128, 128], 0.0)

    # At the cutoff radius, the low-pass response is 0.5.
    assert np.isclose(low[128, 158], 0.5)
    assert np.isclose(high[128, 158], 0.5)

    assert np.allclose(low + high, 1.0)

    print("Butterworth low-pass: PASS")
    print("Butterworth high-pass: PASS")
    print("Butterworth complementarity: PASS")

    print("\n--- Gaussian filter tests ---")

    cutoff = 30

    low = gaussian_low_pass((256, 256), cutoff)
    high = gaussian_high_pass((256, 256), cutoff)

    assert low.shape == (256, 256)
    assert high.shape == (256, 256)

    assert np.isclose(low[128, 128], 1.0)
    assert np.isclose(high[128, 128], 0.0)

    # Gaussian response at D = cutoff.
    expected = np.exp(-0.5)

    assert np.isclose(low[128, 158], expected)
    assert np.isclose(high[128, 158], 1.0 - expected)

    assert np.allclose(low + high, 1.0)

    print("Gaussian low-pass: PASS")
    print("Gaussian high-pass: PASS")
    print("Gaussian complementarity: PASS")

    print("\n--- Band filter tests ---")

    band_pass = ideal_band_pass((256, 256), 15, 60)
    band_stop = ideal_band_stop((256, 256), 15, 60)

    assert band_pass[128, 128] == 0
    assert band_pass[128, 158] == 1
    assert band_pass[128, 208] == 0

    assert band_stop[128, 128] == 1
    assert band_stop[128, 158] == 0
    assert band_stop[128, 208] == 1

    assert np.allclose(band_pass + band_stop, 1.0)

    print("Band-pass: PASS")
    print("Band-stop: PASS")
    print("Band filter complementarity: PASS")

    print("\n--- Notch filter tests ---")

    offsets = [
        (-45, 0), (45, 0),
        (0, -45), (0, 45)
    ]

    notch = ideal_notch_reject((512, 512), offsets, radius=2)

    assert notch[256, 256] == 1.0

    assert notch[211, 256] == 0.0
    assert notch[301, 256] == 0.0
    assert notch[256, 211] == 0.0
    assert notch[256, 301] == 0.0

    assert np.array_equal(
        notch,
        np.roll(np.flip(notch, axis=(0, 1)), (1, 1), axis=(0, 1))
    )

    print("Notch locations: PASS")
    print("Conjugate symmetry: PASS")