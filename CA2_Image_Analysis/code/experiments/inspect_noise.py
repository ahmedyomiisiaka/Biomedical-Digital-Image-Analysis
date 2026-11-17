import numpy as np
from matplotlib import pyplot as plt
from libtiff import TIFF


def read_image(path):
    tif = TIFF.open(path, mode="r")
    image = tif.read_image().astype(float)
    tif.close()
    return image


def inspect_group(name, filenames):
    folder = "data/raw/ImgSetCa2/"

    fig, axes = plt.subplots(2, 3, figsize=(15, 9))

    for column, filename in enumerate(filenames):
        image = read_image(folder + filename)

        spectrum = np.fft.fftshift(np.fft.fft2(image))
        log_magnitude = np.log1p(np.abs(spectrum))

        print(filename)
        print("  Shape:", image.shape)
        print("  Range:", image.min(), image.max())

        axes[0, column].imshow(
            image, cmap="gray", vmin=0, vmax=255
        )
        axes[0, column].set_title(filename)

        axes[1, column].imshow(
            log_magnitude, cmap="gray"
        )
        axes[1, column].set_title("Log Fourier magnitude")

    for ax in axes.flat:
        ax.axis("off")

    plt.tight_layout()

    output = f"results/figures/{name}_noise_spectra.png"
    plt.savefig(output, dpi=200, bbox_inches="tight")
    plt.close(fig)

    print("Saved:", output)


def main():
    inspect_group(
        "kidney",
        [
            "Kidney1-Crop.tif",
            "Kidney1-Crop-Noise1.tif",
            "Kidney1-Crop-Noise2.tif"
        ]
    )

    inspect_group(
        "thorax",
        [
            "Thorax.tif",
            "Thorax-Noise1.tif",
            "Thorax-Noise2.tif"
        ]
    )


if __name__ == "__main__":
    main()