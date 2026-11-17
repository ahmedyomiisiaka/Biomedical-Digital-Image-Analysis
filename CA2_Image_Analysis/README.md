# Compulsory Assignment 2 — Fourier Transform and Frequency-Domain Image Processing

**Course:** Introduction to Image Analysis  
**University:** Vilnius University  
**Programme:** MSc Systems Biology  
**Lecturer:** Allan Rasmusson  
**Assignment:** CA2  
**Programming language:** Python  
**Environment:** Ubuntu Linux (WSL), Conda environment `dia_ca1`

## 1. Project Overview

This project investigates the two-dimensional discrete Fourier transform (DFT), frequency-domain filtering, spatial-domain and frequency-domain equivalence, and the restoration of noisy grayscale images.

The experiments use synthetic grayscale patterns and kidney and thorax TIFF images provided for the assignment.

The project consists of four sections:

- **Section 1.1:** Fourier transformation, zero-padding, frequency shifting, inverse transformation, and image reconstruction.
- **Section 1.2:** Generation of synthetic image patterns and analysis of their Fourier spectra.
- **Section 1.3:** Ideal, Butterworth, Gaussian, band-pass, and band-stop filtering; ringing artifacts; and spatial-frequency equivalence.
- **Section 1.4:** Restoration of two noisy kidney images and two noisy thorax images, including quantitative evaluation against clean reference images.

**Experimental status:** All four sections have been implemented and tested individually. Final submission verification is ongoing.

## 2. Project Structure

```text
CA2_Image_Analysis/
├── README.md
├── code/
│   ├── core/
│   │   ├── fourier_transform.py
│   │   └── frequency_filters.py
│   └── experiments/
│       ├── inspect_kidney.py
│       ├── kidney_fourier.py
│       ├── synthetic_fourier.py
│       ├── ideal_filter_kidney.py
│       ├── butterworth_kidney.py
│       ├── gaussian_kidney.py
│       ├── ringing_comparison.py
│       ├── spatial_frequency_comparison.py
│       ├── gaussian_spatial_comparison.py
│       ├── differentiation_comparison.py
│       ├── band_filter_comparison.py
│       ├── inspect_noise.py
│       ├── noise_baseline.py
│       ├── kidney_noise_peaks.py
│       ├── kidney_notch_restoration.py
│       └── thorax_impulse_restoration.py
├── data/
│   └── raw/
│       └── ImgSetCa2/
├── results/
│   └── figures/
└── report/
    └── CA2_Report_Draft.md
```

The project also contains a backup copy of the synthetic Fourier script. This backup is not required to reproduce the experiments and should be excluded from the final submission.

## 3. Software Requirements

The implementation uses:

- Python 3
- NumPy
- Matplotlib
- TIFF-reading functionality available in the configured environment

The project was developed and tested using Ubuntu Linux through Windows Subsystem for Linux (WSL).

The existing Conda environment is named `dia_ca1`.

### 3.1 Activate the Environment

Open the Ubuntu terminal and navigate to the project directory:

```bash
cd ~/Digital_Image_Analysis/CA2_Image_Analysis
conda activate dia_ca1
```

Configure the Python import path:

```bash
export PYTHONPATH="$PWD/code/core"
```

All experiment commands should be executed from the project root unless otherwise stated.

## 4. Input Data

The original images are stored in:

`data/raw/ImgSetCa2/`

The six principal TIFF files are:

| Filename | Purpose |
|---|---|
| `Kidney1-Crop.tif` | Clean kidney reference image |
| `Kidney1-Crop-Noise1.tif` | Kidney image with periodic interference |
| `Kidney1-Crop-Noise2.tif` | Kidney image with periodic interference |
| `Thorax.tif` | Clean thorax reference image |
| `Thorax-Noise1.tif` | Thorax image with impulse-like noise |
| `Thorax-Noise2.tif` | Thorax image with distributed additive noise |

The images used in the principal experiments have dimensions of 512 × 512 pixels.

Original image files are kept separate from the generated figures and analysis results.

## 5. Section 1.1 — Fourier Transform and Image Reconstruction

### 5.1 Run the Experiments

```bash
python code/core/fourier_transform.py
python code/experiments/kidney_fourier.py
```

The processing pipeline performs the following operations:

1. Read the original grayscale kidney image.
2. Zero-pad the image from 512 × 512 to 1024 × 1024 pixels.
3. Apply periodicity shifting using multiplication by `(-1)^(r+c)`.
4. Calculate the two-dimensional Fourier transform.
5. Apply the inverse Fourier transform and reverse the periodicity shift.
6. Crop the reconstructed image to the original dimensions.

### 5.2 Results

| Measurement | Result |
|---|---:|
| Original dimensions | 512 × 512 |
| Padded dimensions | 1024 × 1024 |
| Maximum absolute reconstruction error | 1.7053 × 10⁻¹³ |
| Mean absolute reconstruction error | 2.4484 × 10⁻¹⁴ |

Additional tests included non-square images, constant-intensity images, and single-pixel patterns.

The reconstruction tests passed.

**Generated figure:**

`results/figures/kidney_six_stages.png`

## 6. Section 1.2 — Synthetic Fourier Experiments

### 6.1 Run the Experiment

```bash
python code/experiments/synthetic_fourier.py
```

Four synthetic images were generated, each measuring 256 × 256 pixels.

| Image | Row frequency | Column frequency |
|---|---:|---:|
| Constant intensity | 0 | 0 |
| Vertical cosine stripes | 0 | 8 |
| Horizontal cosine stripes | 8 | 0 |
| Diagonal cosine stripes | 6 | 8 |

The constant image had intensity 128.

For the cosine images, the background intensity was 128 and the amplitude was 100.

### 6.2 Results

The calculated Fourier spectra agreed with the theoretical predictions.

The constant image produced only the DC component.

Vertical stripes produced frequency peaks displaced along the horizontal frequency axis, while horizontal stripes produced peaks displaced along the vertical frequency axis.

The diagonal pattern produced symmetric peaks displaced along both frequency axes.

The numerical peak-validation tests passed.

**Generated figures:**

- `results/figures/constant_fourier.png`
- `results/figures/vertical_stripes_fourier.png`
- `results/figures/horizontal_stripes_fourier.png`
- `results/figures/diagonal_stripes_fourier.png`

## 7. Section 1.3 — Frequency-Domain Filtering

### 7.1 Frequency Filter Functions

Run the core filter tests:

```bash
python code/core/frequency_filters.py
```

The implemented functions include:

- Ideal low-pass and high-pass filters
- Butterworth low-pass and high-pass filters
- Gaussian low-pass and high-pass filters
- Ideal band-pass and band-stop filters
- Ideal notch-reject filters

The tests examine filter construction, complementary frequency responses, and numerical behavior.

### 7.2 Ideal Low-Pass and High-Pass Filtering

```bash
python code/experiments/ideal_filter_kidney.py
```

The clean kidney image was filtered using an ideal cutoff radius of 30 frequency pixels.

Low-pass filtering reduced fine details, while high-pass filtering emphasized boundaries and rapid intensity changes.

Abrupt frequency cutoffs also produced visible ringing artifacts.

**Figure:** `results/figures/ideal_filter_kidney.png`

### 7.3 Butterworth Filtering

```bash
python code/experiments/butterworth_kidney.py
```

Butterworth orders 1, 2, and 4 were compared using a cutoff radius of 30.

Increasing the filter order produced a steeper frequency transition.

The complementary low-pass and high-pass outputs reconstructed the original image to floating-point precision.

**Figure:** `results/figures/butterworth_kidney.png`

### 7.4 Gaussian Filtering

```bash
python code/experiments/gaussian_kidney.py
```

Gaussian low-pass and high-pass filters were evaluated using a frequency-distance parameter of 30.

The Gaussian filter produced a gradual transition between retained and attenuated frequencies.

Compared with ideal filtering, the low-pass output showed less visually apparent ringing.

**Figure:** `results/figures/gaussian_kidney.png`

### 7.5 Ringing Artifact Comparison

```bash
python code/experiments/ringing_comparison.py
```

A synthetic 256 × 256 image was generated with intensities of 50 and 200 on opposite sides of a sharp boundary.

Four low-pass filters were compared using a frequency-distance parameter of 20.

| Filter | Undershoot | Overshoot |
|---|---:|---:|
| Ideal | 13.616654 | 13.616654 |
| Butterworth order 2 | 5.033053 | 5.033053 |
| Butterworth order 4 | 10.288823 | 10.288823 |
| Gaussian | 0.000000 | 0.000000 |

The ideal filter produced the largest ringing.

The Gaussian filter produced no measurable overshoot or undershoot beyond the original intensity range in this experiment, although it blurred the sharp boundary.

**Generated figures:**

- `results/figures/ringing_profiles.png`
- `results/figures/ringing_measurements.png`

### 7.6 Spatial and Frequency-Domain Averaging

```bash
python code/experiments/spatial_frequency_comparison.py
```

A 3 × 3 averaging filter was implemented using direct spatial averaging and Fourier-domain multiplication.

Both methods used periodic boundary conditions.

The maximum absolute difference for the kidney image was:

`1.7053e-13`

The numerical equivalence test passed.

**Figure:** `results/figures/spatial_frequency_kidney.png`

**Note:** This script currently saves its figure in the project root. Move the figure to `results/figures/` after rerunning it, unless the output path has been corrected.

### 7.7 Spatial and Frequency-Domain Gaussian Smoothing

```bash
python code/experiments/gaussian_spatial_comparison.py
```

A normalized 13 × 13 Gaussian kernel with a standard deviation of 2 pixels was used.

The spatial and frequency-domain implementations used the same discrete kernel and periodic boundary conditions.

The maximum absolute difference was:

`3.9790e-13`

The numerical equivalence test passed.

**Figure:** `results/figures/gaussian_spatial_frequency.png`

### 7.8 Spatial and Frequency-Domain Differentiation

```bash
python code/experiments/differentiation_comparison.py
```

A horizontal forward-difference operator was implemented in the spatial and frequency domains.

The maximum absolute difference was:

`9.9476e-14`

The numerical equivalence test passed.

**Figure:** `results/figures/differentiation_comparison.png`

### 7.9 Band-Pass and Band-Stop Filtering

```bash
python code/experiments/band_filter_comparison.py
```

Ideal band-pass and band-stop filters were applied using inner and outer radii of 15 and 60 frequency pixels.

The band-pass filter retained intermediate spatial frequencies, while the band-stop filter suppressed the same interval.

The maximum reconstruction error from adding the complementary outputs was:

`1.6342e-13`

**Figure:** `results/figures/band_filter_kidney.png`

## 8. Section 1.4 — Noisy Image Restoration

**Status: Completed.**

Two noisy kidney images and two noisy thorax images were investigated.

Restoration performance was evaluated against the corresponding clean reference images using:

- Mean squared error (MSE)
- Mean absolute error (MAE)
- Peak signal-to-noise ratio (PSNR)

### 8.1 Noise Inspection and Baseline Measurements

```bash
python code/experiments/inspect_noise.py
python code/experiments/noise_baseline.py
python code/experiments/kidney_noise_peaks.py
```

The noisy images were compared with their clean references to examine residual noise and Fourier characteristics.

The kidney images contained periodic interference with identifiable spectral peaks.

Thorax Noise1 showed impulse-like corruption, while Thorax Noise2 showed approximately zero-mean distributed noise.

The Thorax Noise2 residual had a mean of approximately −0.0081 and a standard deviation of 6.9890. These observations are consistent with additive noise but do not establish a specific probability distribution.

**Diagnostic figures:**

- `results/figures/kidney_noise_spectra.png`
- `results/figures/thorax_noise_spectra.png`
- `results/figures/kidney_noise1_residual_spectrum.png`
- `results/figures/kidney_noise2_residual_spectrum.png`

### 8.2 Kidney Noise1 and Noise2 Restoration

```bash
python code/experiments/kidney_notch_restoration.py
```

Symmetric ideal notch-reject filters were applied to suppress periodic interference.

Notch radii of 1, 2, 3, and 5 pixels were evaluated.

| Image | Best tested radius | MSE before | MSE after | PSNR before | PSNR after |
|---|---:|---:|---:|---:|---:|
| Kidney Noise1 | 5 | 18.3355 | 1.7705 | 35.4979 dB | 45.6498 dB |
| Kidney Noise2 | 1 | 18.3085 | 1.3504 | 35.5043 dB | 46.8263 dB |

Kidney Noise1 achieved a PSNR improvement of approximately 10.15 dB.

Kidney Noise2 achieved a PSNR improvement of approximately 11.32 dB.

**Generated figures:**

- `results/figures/kidney_noise1_notch_restoration.png`
- `results/figures/kidney_noise2_notch_restoration.png`

The clean kidney reference was used to diagnose interference frequencies and evaluate the tested filter parameters. These results therefore represent reference-assisted restoration.

### 8.3 Thorax Noise1 — Impulse-Like Noise

```bash
python code/experiments/thorax_impulse_restoration.py
```

Arithmetic averaging and median filters were compared using 3 × 3 and 5 × 5 neighborhoods.

| Method | MSE | MAE | PSNR |
|---|---:|---:|---:|
| Noisy image | 2420.7914 | 18.7080 | 14.2912 dB |
| Averaging 3 × 3 | 478.4741 | 15.7122 | 21.3322 dB |
| Averaging 5 × 5 | 327.3604 | 15.2745 | 22.9805 dB |
| Median 3 × 3 | 64.8105 | 7.4979 | 30.0143 dB |
| Median 5 × 5 | 61.8313 | 7.4963 | 30.2187 dB |

The 5 × 5 median filter produced the lowest MSE and highest PSNR among the tested methods.

The PSNR improvement was approximately 15.93 dB.

**Figure:** `results/figures/thorax_noise1_median_restoration.png`

Median filtering was more effective than arithmetic averaging for this impulse-like noise pattern.

### 8.4 Thorax Noise2 — Distributed Noise

The same restoration script evaluates arithmetic averaging and Gaussian smoothing for Thorax Noise2.

Gaussian filters were tested with different kernel sizes and standard deviations.

| Method | MSE | MAE | PSNR |
|---|---:|---:|---:|
| Noisy image | 48.8465 | 5.5662 | 31.2425 dB |
| Averaging 3 × 3 | 6.2907 | 1.9798 | 40.1438 dB |
| Averaging 5 × 5 | 6.5697 | 1.7018 | 39.9554 dB |
| Gaussian 3 × 3, σ = 0.8 | 7.7546 | 2.2179 | 39.2352 dB |
| Gaussian 3 × 3, σ = 1.0 | 6.7255 | 2.0601 | 39.8535 dB |
| Gaussian 5 × 5, σ = 1.0 | 5.2923 | 1.7866 | 40.8943 dB |
| Gaussian 5 × 5, σ = 1.5 | 5.0478 | 1.6198 | 41.0998 dB |

The Gaussian 5 × 5 filter with σ = 1.5 produced the lowest MSE and highest PSNR among the tested configurations.

The PSNR improvement was approximately 9.86 dB.

**Figure:** `results/figures/thorax_noise2_restoration.png`

### 8.5 Overall Restoration Comparison

| Image | Best tested method | MSE before | MSE after | PSNR improvement |
|---|---|---:|---:|---:|
| Kidney Noise1 | Ideal notch, radius 5 | 18.3355 | 1.7705 | +10.15 dB |
| Kidney Noise2 | Ideal notch, radius 1 | 18.3085 | 1.3504 | +11.32 dB |
| Thorax Noise1 | Median 5 × 5 | 2420.7914 | 61.8313 | +15.93 dB |
| Thorax Noise2 | Gaussian 5 × 5, σ = 1.5 | 48.8465 | 5.0478 | +9.86 dB |

All four noisy images showed substantial quantitative improvement.

The results demonstrate that different noise patterns require different restoration approaches.

The best configurations were selected from the tested parameters using clean reference images. They should not be interpreted as universally optimal settings.

## 9. Scientific Report

The scientific report is located at:

`report/CA2_Report_Draft.md`

It contains the theoretical background, methods, experimental figures, numerical results, discussions, and conclusions for Sections 1.1–1.4.

The report includes 18 numbered figures.

The figure files are stored in:

`results/figures/`

## 10. Reproducibility

To reproduce the experiments, open the Ubuntu terminal and run:

```bash
cd ~/Digital_Image_Analysis/CA2_Image_Analysis
conda activate dia_ca1
export PYTHONPATH="$PWD/code/core"
```

Run the core tests:

```bash
python code/core/fourier_transform.py
python code/core/frequency_filters.py
```

Run the Section 1.1 and 1.2 experiments:

```bash
python code/experiments/kidney_fourier.py
python code/experiments/synthetic_fourier.py
```

Run the Section 1.3 experiments:

```bash
python code/experiments/ideal_filter_kidney.py
python code/experiments/butterworth_kidney.py
python code/experiments/gaussian_kidney.py
python code/experiments/ringing_comparison.py
python code/experiments/spatial_frequency_comparison.py
python code/experiments/gaussian_spatial_comparison.py
python code/experiments/differentiation_comparison.py
python code/experiments/band_filter_comparison.py
```

Run the Section 1.4 experiments:

```bash
python code/experiments/inspect_noise.py
python code/experiments/noise_baseline.py
python code/experiments/kidney_noise_peaks.py
python code/experiments/kidney_notch_restoration.py
python code/experiments/thorax_impulse_restoration.py
```

The experiment scripts generate numerical results and figures used in the scientific report.

Most generated figures are saved in `results/figures/`. The spatial-frequency averaging script currently writes its figure to the project root; move it into the figures directory after execution.

The image-processing calculations retain floating-point values where necessary. Display offsets applied to signed high-pass and band-pass images do not alter the underlying numerical results.

## 11. Project Status

| Section | Status |
|---|---|
| 1.1 Fourier transform and reconstruction | Completed |
| 1.2 Synthetic Fourier experiments | Completed |
| 1.3 Frequency-domain filtering | Completed |
| 1.4 Noisy image restoration | Completed |
| Scientific report | Updated |
| Final reproducibility and submission audit | Pending |

All four assignment sections have been implemented and individually tested. Final verification of the complete submission package remains to be performed.

## 12. Summary

This project demonstrates how Fourier analysis can be used to understand spatial image patterns, apply frequency-selective filters, and reconstruct grayscale images.

The spatial-frequency comparisons showed numerical agreement to floating-point precision when equivalent operations and boundary conditions were used.

The ringing experiments highlighted the effects of abrupt frequency cutoffs.

The restoration experiments showed that notch filtering was effective for periodic interference, median filtering for impulse-like noise, and Gaussian smoothing for distributed noise.

Overall, the experiments demonstrate the importance of choosing image-processing methods according to the mathematical properties of the filter and the characteristics of the image and noise.