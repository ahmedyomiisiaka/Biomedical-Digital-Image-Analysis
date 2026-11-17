import numpy as np
from libtiff import TIFF


def read_image(filename):
    path = "data/raw/ImgSetCa2/" + filename

    tif = TIFF.open(path, mode="r")
    image = tif.read_image().astype(float)
    tif.close()

    return image


def calculate_metrics(reference, test):
    if reference.shape != test.shape:
        raise ValueError("Image dimensions must match")

    difference = reference - test

    mse = np.mean(difference ** 2)
    mae = np.mean(np.abs(difference))

    if mse == 0:
        psnr = float("inf")
    else:
        psnr = 10 * np.log10((255.0 ** 2) / mse)

    return mse, mae, psnr


def main():
    comparisons = [
        ("Kidney1-Crop.tif", "Kidney1-Crop-Noise1.tif"),
        ("Kidney1-Crop.tif", "Kidney1-Crop-Noise2.tif"),
        ("Thorax.tif", "Thorax-Noise1.tif"),
        ("Thorax.tif", "Thorax-Noise2.tif")
    ]

    for clean_name, noisy_name in comparisons:
        clean = read_image(clean_name)
        noisy = read_image(noisy_name)

        mse, mae, psnr = calculate_metrics(clean, noisy)

        print("\nImage:", noisy_name)
        print("MSE:", f"{mse:.6f}")
        print("MAE:", f"{mae:.6f}")
        print("PSNR:", f"{psnr:.4f}", "dB")


if __name__ == "__main__":
    main()