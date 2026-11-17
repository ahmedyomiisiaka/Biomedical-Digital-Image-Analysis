
import numpy as np
from matplotlib import pyplot as plt
from libtiff import TIFF

from frequency_filters import ideal_notch_reject
from ideal_filter_kidney import apply_frequency_filter


DATA_FOLDER = "data/raw/ImgSetCa2/"
RESULTS_FOLDER = "results/figures/"

RADII = [1, 2, 3, 5]


def read_image(filename):
    tif = TIFF.open(DATA_FOLDER + filename, mode="r")
    image = tif.read_image().astype(float)
    tif.close()
    return image


def calculate_metrics(reference, image):
    difference = reference - image

    mse = np.mean(difference ** 2)
    mae = np.mean(np.abs(difference))

    if mse == 0:
        psnr = float("inf")
    else:
        psnr = 10 * np.log10(255.0 ** 2 / mse)

    return mse, mae, psnr


def restore_image(noisy, offsets, radius):
    mask = ideal_notch_reject(
        noisy.shape,
        offsets,
        radius
    )

    restored = apply_frequency_filter(noisy, mask)

    return restored, mask


def analyse_image(clean, noisy, offsets, name):
    print("\n" + "=" * 55)
    print("Experiment:", name)
    print("=" * 55)

    baseline_mse, baseline_mae, baseline_psnr = (
        calculate_metrics(clean, noisy)
    )

    print(
        f"Baseline: MSE={baseline_mse:.6f}, "
        f"MAE={baseline_mae:.6f}, "
        f"PSNR={baseline_psnr:.4f} dB"
    )

    results = []

    for radius in RADII:
        restored, mask = restore_image(
            noisy,
            offsets,
            radius
        )

        mse, mae, psnr = calculate_metrics(
            clean,
            restored
        )

        results.append(
            (radius, restored, mask, mse, mae, psnr)
        )

        print(
            f"Radius {radius}: "
            f"MSE={mse:.6f}, "
            f"MAE={mae:.6f}, "
            f"PSNR={psnr:.4f} dB"
        )

    best = min(results, key=lambda item: item[3])

    best_radius = best[0]
    best_image = best[1]
    best_mask = best[2]
    best_mse = best[3]
    best_psnr = best[5]

    print("\nBest tested radius:", best_radius)
    print("Best MSE:", f"{best_mse:.6f}")
    print("Best PSNR:", f"{best_psnr:.4f}", "dB")
    print(
        "PSNR improvement:",
        f"{best_psnr - baseline_psnr:+.4f}",
        "dB"
    )

    fig, axes = plt.subplots(2, 3, figsize=(15, 10))

    images = [
        clean,
        noisy,
        best_image,
        np.log1p(
            np.abs(np.fft.fftshift(np.fft.fft2(noisy)))
        ),
        best_mask,
        np.abs(clean - best_image)
    ]

    titles = [
        "Clean reference",
        "Noisy image",
        f"Restored (radius={best_radius})",
        "Noisy Fourier spectrum",
        "Notch-reject mask",
        "Absolute restoration error"
    ]

    for index, ax in enumerate(axes.flat):
        if index < 3:
            ax.imshow(
                images[index],
                cmap="gray",
                vmin=0,
                vmax=255
            )
        elif index == 4:
            ax.imshow(
                images[index],
                cmap="gray",
                vmin=0,
                vmax=1
            )
        else:
            ax.imshow(images[index], cmap="gray")

        ax.set_title(titles[index])
        ax.axis("off")

    plt.tight_layout()

    output = (
        RESULTS_FOLDER
        + name
        + "_notch_restoration.png"
    )

    plt.savefig(
        output,
        dpi=200,
        bbox_inches="tight"
    )

    plt.close(fig)

    print("Figure saved:", output)

    return results


def main():
    clean = read_image("Kidney1-Crop.tif")

    noise1 = read_image(
        "Kidney1-Crop-Noise1.tif"
    )

    noise2 = read_image(
        "Kidney1-Crop-Noise2.tif"
    )

    assert clean.shape == noise1.shape
    assert clean.shape == noise2.shape

    noise1_offsets = [
        (-190, 0), (190, 0),
        (0, -190), (0, 190),
        (-134, -134), (134, 134),
        (-134, 134), (134, -134)
    ]

    noise2_offsets = [
        (-45, 0), (45, 0),
        (0, -45), (0, 45),
        (-32, -32), (32, 32),
        (-32, 32), (32, -32)
    ]

    analyse_image(
        clean,
        noise1,
        noise1_offsets,
        "kidney_noise1"
    )

    analyse_image(
        clean,
        noise2,
        noise2_offsets,
        "kidney_noise2"
    )

    print("\nKidney notch restoration experiments completed.")


if __name__ == "__main__":
    main()
