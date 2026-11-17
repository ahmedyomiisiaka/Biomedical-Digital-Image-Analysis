import os

import numpy as np
from libtiff import TIFF
from matplotlib import pyplot as plt


def median_filter(image, window_size=3):
    """Apply a median filter using reflected image boundaries."""

    if image.ndim != 2:
        raise ValueError("Image must be two-dimensional")

    if window_size < 3 or window_size % 2 == 0:
        raise ValueError("Window size must be odd and at least 3")

    radius = window_size // 2

    padded = np.pad(
        image,
        pad_width=radius,
        mode="reflect"
    )

    result = np.zeros_like(image, dtype=float)

    for row in range(image.shape[0]):
        for col in range(image.shape[1]):

            neighbourhood = padded[
                row:row + window_size,
                col:col + window_size
            ]

            result[row, col] = np.median(neighbourhood)

    return result


def averaging_filter(image, window_size=3):
    radius = window_size // 2
    padded = np.pad(image, radius, mode="reflect")
    result = np.zeros_like(image, dtype=float)

    for row in range(image.shape[0]):
        for col in range(image.shape[1]):
            neighbourhood = padded[
                row:row + window_size,
                col:col + window_size
            ]
            result[row, col] = np.mean(neighbourhood)

    return result


def gaussian_filter(image, window_size=3, sigma=1.0):
    """Apply a spatial Gaussian filter using reflected boundaries."""

    if window_size < 3 or window_size % 2 == 0:
        raise ValueError("Window size must be odd and at least 3")

    if sigma <= 0:
        raise ValueError("Sigma must be positive")

    radius = window_size // 2

    offsets = np.arange(-radius, radius + 1)
    x, y = np.meshgrid(offsets, offsets)

    kernel = np.exp(-(x ** 2 + y ** 2) / (2 * sigma ** 2))
    kernel = kernel / kernel.sum()

    padded = np.pad(image, radius, mode="reflect")
    result = np.zeros_like(image, dtype=float)

    for row in range(image.shape[0]):
        for col in range(image.shape[1]):
            neighbourhood = padded[
                row:row + window_size,
                col:col + window_size
            ]
            result[row, col] = np.sum(neighbourhood * kernel)

    return result


def read_image(filename):
    tif = TIFF.open("data/raw/ImgSetCa2/" + filename, mode="r")
    image = tif.read_image().astype(float)
    tif.close()
    return image


def calculate_metrics(reference, test):
    mse = np.mean((reference - test) ** 2)
    mae = np.mean(np.abs(reference - test))
    psnr = float("inf") if mse == 0 else 10 * np.log10(255**2 / mse)
    return mse, mae, psnr


def main():
    clean = read_image("Thorax.tif")
    noisy = read_image("Thorax-Noise1.tif")

    assert clean.shape == noisy.shape

    median3 = median_filter(noisy, 3)
    median5 = median_filter(noisy, 5)

    average3 = averaging_filter(noisy, 3)
    average5 = averaging_filter(noisy, 5)

    for name, image in [
        ("Average 3x3", average3),
        ("Average 5x5", average5)
    ]:
        mse, mae, psnr = calculate_metrics(clean, image)
        print(
            f"{name}: MSE={mse:.6f}, "
            f"MAE={mae:.6f}, PSNR={psnr:.4f} dB"
        )

    images = [clean, noisy, median3, median5]

    names = [
        "Clean reference",
        "Noisy thorax",
        "Median 3x3",
        "Median 5x5"
    ]

    for name, image in zip(names[1:], images[1:]):
        mse, mae, psnr = calculate_metrics(clean, image)
        print(
            f"{name}: MSE={mse:.6f}, "
            f"MAE={mae:.6f}, PSNR={psnr:.4f} dB"
        )

    fig, axes = plt.subplots(1, 4, figsize=(16, 5))

    for ax, image, title in zip(axes, images, names):
        ax.imshow(image, cmap="gray", vmin=0, vmax=255)
        ax.set_title(title)
        ax.axis("off")

    plt.tight_layout()

    os.makedirs("results/figures", exist_ok=True)

    plt.savefig(
        "results/figures/thorax_noise1_median_restoration.png",
        dpi=200,
        bbox_inches="tight"
    )
    plt.close(fig)

    print("Figure saved successfully.")

    noisy2 = read_image("Thorax-Noise2.tif")

    print("\n--- Thorax Noise2 ---")

    for size in [3, 5]:
        restored = averaging_filter(noisy2, size)
        mse, mae, psnr = calculate_metrics(clean, restored)
        print(
            f"Average {size}x{size}: "
            f"MSE={mse:.6f}, "
            f"MAE={mae:.6f}, "
            f"PSNR={psnr:.4f} dB"
        )

    print("\n--- Thorax Noise2: Gaussian filtering ---")

    for size, sigma in [(3, 0.8), (3, 1.0), (5, 1.0), (5, 1.5)]:
        restored = gaussian_filter(noisy2, size, sigma)
        mse, mae, psnr = calculate_metrics(clean, restored)
        print(
            f"Gaussian {size}x{size}, sigma={sigma}: "
            f"MSE={mse:.6f}, "
            f"MAE={mae:.6f}, "
            f"PSNR={psnr:.4f} dB"
        )

    best_gaussian = gaussian_filter(noisy2, 5, 1.5)
    average3_noise2 = averaging_filter(noisy2, 3)

    images = [
        clean,
        noisy2,
        average3_noise2,
        best_gaussian
    ]

    titles = [
        "Clean reference",
        "Thorax Noise2",
        "Average 3x3",
        "Gaussian 5x5 (sigma=1.5)"
    ]

    fig, axes = plt.subplots(1, 4, figsize=(16, 5))

    for ax, image, title in zip(axes, images, titles):
        ax.imshow(
            image,
            cmap="gray",
            vmin=0,
            vmax=255
        )
        ax.set_title(title)
        ax.axis("off")

    plt.tight_layout()

    plt.savefig(
        "results/figures/thorax_noise2_restoration.png",
        dpi=200,
        bbox_inches="tight"
    )
    plt.close(fig)

    print("Thorax Noise2 comparison figure saved.")


if __name__ == "__main__":
    main()