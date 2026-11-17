import numpy as np
from libtiff import TIFF
from matplotlib import pyplot as plt


def spatial_average(image):
    """Apply a 3x3 averaging filter with periodic boundaries."""

    height, width = image.shape

    output = np.zeros((height, width), dtype=float)

    for row in range(height):
        for col in range(width):

            total = 0.0

            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:

                    rr = (row + dr) % height
                    cc = (col + dc) % width

                    total += image[rr, cc]

            output[row, col] = total / 9.0

    return output


def frequency_average(image):
    """Apply the same 3x3 averaging filter using the FFT."""

    height, width = image.shape

    kernel = np.zeros((height, width), dtype=float)

    # Position the kernel around the circular origin.
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:

            rr = dr % height
            cc = dc % width

            kernel[rr, cc] = 1.0 / 9.0

    image_fft = np.fft.fft2(image)
    kernel_fft = np.fft.fft2(kernel)

    filtered = np.fft.ifft2(image_fft * kernel_fft)

    return filtered.real


def main():

    image = np.array(
        [
            [10, 20, 30, 40, 50],
            [15, 25, 35, 45, 55],
            [20, 30, 40, 50, 60],
            [25, 35, 45, 55, 65],
            [30, 40, 50, 60, 70]
        ],
        dtype=float
    )

    spatial_result = spatial_average(image)
    frequency_result = frequency_average(image)

    error = np.max(
        np.abs(spatial_result - frequency_result)
    )

    print("Original image:")
    print(image)

    print("\nSpatial averaging:")
    print(spatial_result)

    print("\nFrequency-domain averaging:")
    print(frequency_result)

    print("\nMaximum absolute difference:", error)

    assert error < 1e-10

    print("Spatial-frequency equivalence: PASS")


def kidney_comparison():

    image_path = "data/raw/ImgSetCa2/Kidney1-Crop.tif"

    tif = TIFF.open(image_path, mode="r")
    image = tif.read_image().astype(float)
    tif.close()

    spatial_result = spatial_average(image)
    frequency_result = frequency_average(image)

    difference = np.abs(spatial_result - frequency_result)

    max_error = np.max(difference)
    mean_error = np.mean(difference)

    print("\n--- Kidney image comparison ---")
    print("Image dimensions:", image.shape)
    print("Maximum absolute difference:", max_error)
    print("Mean absolute difference:", mean_error)

    assert max_error < 1e-10

    fig, axes = plt.subplots(1, 4, figsize=(18, 5))

    images = [
        image,
        spatial_result,
        frequency_result,
        difference
    ]

    titles = [
        "Original kidney",
        "Spatial 3x3 averaging",
        "Frequency-domain averaging",
        "Absolute difference"
    ]

    for index, axis in enumerate(axes):

        if index == 3:
            axis.imshow(
                images[index],
                cmap="gray",
                interpolation="nearest"
            )
        else:
            axis.imshow(
                images[index],
                cmap="gray",
                vmin=0,
                vmax=255,
                interpolation="nearest"
            )

        axis.set_title(titles[index])
        axis.axis("off")

    plt.tight_layout()
    plt.savefig("spatial_frequency_kidney.png", dpi=200)
    plt.close(fig)

    print("Figure saved: spatial_frequency_kidney.png")


if __name__ == "__main__":
    main()
    kidney_comparison()