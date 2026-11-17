import numpy as np
from matplotlib import pyplot as plt
from libtiff import TIFF


def read_image(filename):
    path = "data/raw/ImgSetCa2/" + filename

    tif = TIFF.open(path, mode="r")
    image = tif.read_image().astype(float)
    tif.close()

    return image


def analyse_noise(clean, noisy, name):
    residual = noisy - clean

    spectrum = np.fft.fftshift(np.fft.fft2(residual))
    magnitude = np.abs(spectrum)

    height, width = magnitude.shape
    centre_row = height // 2
    centre_col = width // 2

    # Exclude the low-frequency region around the centre.
    rows, cols = np.indices(magnitude.shape)

    distance = np.sqrt(
        (rows - centre_row) ** 2
        + (cols - centre_col) ** 2
    )

    candidates = magnitude.copy()
    candidates[distance < 10] = 0

    # Display the strongest frequency coordinates.
    indices = np.argsort(candidates.ravel())[-12:][::-1]

    print(f"\n{name}: strongest residual frequencies")

    for index in indices:
        row, col = np.unravel_index(index, magnitude.shape)

        print(
            f"Offset ({row-centre_row:+d}, "
            f"{col-centre_col:+d}), "
            f"magnitude={magnitude[row, col]:.2f}"
        )

    fig, axes = plt.subplots(1, 2, figsize=(11, 5))

    axes[0].imshow(
        residual, cmap="gray",
        vmin=-30, vmax=30
    )
    axes[0].set_title("Noise residual")

    axes[1].imshow(
        np.log1p(magnitude), cmap="gray"
    )
    axes[1].set_title("Residual Fourier spectrum")

    for ax in axes:
        ax.axis("off")

    plt.tight_layout()

    output = f"results/figures/{name}_residual_spectrum.png"
    plt.savefig(output, dpi=200, bbox_inches="tight")
    plt.close()

    print("Saved:", output)


def main():
    clean = read_image("Kidney1-Crop.tif")

    for name, filename in [
        ("kidney_noise1", "Kidney1-Crop-Noise1.tif"),
        ("kidney_noise2", "Kidney1-Crop-Noise2.tif")
    ]:
        noisy = read_image(filename)

        assert clean.shape == noisy.shape

        analyse_noise(clean, noisy, name)


if __name__ == "__main__":
    main()