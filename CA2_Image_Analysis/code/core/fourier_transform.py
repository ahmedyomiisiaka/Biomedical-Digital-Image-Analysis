import numpy as np


def _check_image(image, name="image"):
    """Validate a non-empty, numeric, two-dimensional NumPy array."""
    if not isinstance(image, np.ndarray):
        raise TypeError(f"{name} must be a NumPy array")

    if image.ndim != 2 or image.size == 0:
        raise ValueError(f"{name} must be a non-empty 2D array")

    if not np.issubdtype(image.dtype, np.number):
        raise TypeError(f"{name} must contain numeric values")


def _check_shape(shape, name="shape"):
    """Validate a pair of positive integer dimensions."""
    if not isinstance(shape, (tuple, list)) or len(shape) != 2:
        raise TypeError(f"{name} must contain two integers")

    for dimension in shape:
        if isinstance(dimension, (bool, np.bool_)):
            raise TypeError(f"{name} must contain integers")

        if not isinstance(dimension, (int, np.integer)):
            raise TypeError(f"{name} must contain integers")

        if dimension <= 0:
            raise ValueError(f"{name} dimensions must be positive")


def zero_pad_image(image, pad_shape=None):
    """Zero-pad a 2D image, retaining the original in the upper-left corner."""
    _check_image(image)

    if pad_shape is None:
        pad_shape = (
            2 * image.shape[0],
            2 * image.shape[1]
        )

    _check_shape(pad_shape, "pad_shape")

    if (
        pad_shape[0] < image.shape[0]
        or pad_shape[1] < image.shape[1]
    ):
        raise ValueError("Padded dimensions cannot be smaller than the image")

    padded = np.zeros(pad_shape, dtype=image.dtype)

    padded[:image.shape[0], :image.shape[1]] = image

    return padded


def shift_periodicity(image):
    """Multiply a 2D image by (-1)^(row+column)."""
    _check_image(image)

    if np.iscomplexobj(image):
        values = image
    else:
        values = image.astype(np.float64)

    rows, columns = np.indices(image.shape)

    signs = 1 - 2 * ((rows + columns) % 2)

    return values * signs


def forward_fourier(image):
    """Calculate the two-dimensional discrete Fourier transform."""
    _check_image(image)

    return np.fft.fft2(image)


def inverse_fourier(spectrum):
    """Calculate the inverse DFT with NumPy's default normalization."""
    _check_image(spectrum, "spectrum")

    return np.fft.ifft2(spectrum)


def crop_image(image, original_shape):
    """Crop an image to its original dimensions from the upper-left corner."""
    _check_image(image)
    _check_shape(original_shape, "original_shape")

    if (
        original_shape[0] > image.shape[0]
        or original_shape[1] > image.shape[1]
    ):
        raise ValueError("Original dimensions exceed image dimensions")

    return image[
        :original_shape[0],
        :original_shape[1]
    ]


if __name__ == "__main__":

    print("--- Zero-padding test ---")

    small = np.array([
        [1, 2],
        [3, 4]
    ])

    padded = zero_pad_image(small)

    assert padded.shape == (4, 4)
    assert np.array_equal(padded[:2, :2], small)

    print("Zero padding: PASS")

    print("\n--- Periodicity-shifting test ---")

    shifted = shift_periodicity(small)

    expected = np.array([
        [1, -2],
        [-3, 4]
    ])

    assert np.array_equal(shifted, expected)

    print("Periodicity shifting: PASS")

    print("\n--- Complex-input test ---")

    complex_image = np.array([
        [1 + 1j, 2],
        [3, 4]
    ])

    complex_shifted = shift_periodicity(complex_image)

    complex_expected = np.array([
        [1 + 1j, -2],
        [-3, 4]
    ])

    assert np.array_equal(complex_shifted, complex_expected)

    print("Complex input preserved: PASS")

    print("\n--- Fourier reconstruction test ---")

    padded = zero_pad_image(small)

    shifted = shift_periodicity(padded)

    spectrum = forward_fourier(shifted)

    inverse = inverse_fourier(spectrum)

    max_imaginary = np.max(np.abs(inverse.imag))

    assert max_imaginary < 1e-10

    unshifted = shift_periodicity(inverse.real)

    reconstructed = crop_image(unshifted, small.shape)

    error = np.abs(
        small.astype(np.float64) - reconstructed
    )

    max_error = np.max(error)
    mean_error = np.mean(error)

    assert np.allclose(
        small,
        reconstructed,
        atol=1e-10,
        rtol=0
    )

    print("Maximum imaginary residual:", max_imaginary)
    print("Maximum reconstruction error:", max_error)
    print("Mean absolute error:", mean_error)
    print("Fourier reconstruction: PASS")

    print("\n--- Invalid-input tests ---")

    bad_cases = [
        (
            "Negative crop dimension",
            lambda: crop_image(np.ones((10, 10)), (-1, 5))
        ),
        (
            "Zero crop dimension",
            lambda: crop_image(np.ones((10, 10)), (0, 5))
        ),
        (
            "Oversized crop",
            lambda: crop_image(np.ones((10, 10)), (20, 5))
        ),
        (
            "Undersized padding",
            lambda: zero_pad_image(np.ones((10, 10)), (5, 5))
        ),
        (
            "String padding shape",
            lambda: zero_pad_image(np.ones((4, 4)), "ab")
        ),
        (
            "Floating-point dimensions",
            lambda: zero_pad_image(np.ones((4, 4)), (8.0, 8.0))
        ),
        (
            "Non-numeric image",
            lambda: shift_periodicity(np.array([["a", "b"]]))
        ),
    ]

    for label, test_function in bad_cases:
        try:
            test_function()
        except (TypeError, ValueError):
            print(f"{label}: PASS")
        else:
            raise AssertionError(
                f"{label}: invalid input was not rejected"
            )

    print("\nAll core validation tests passed.")