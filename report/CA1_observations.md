# Compulsory Assignment 1 — Image Analysis

## Part 1: TIFF image investigation

### Kidney1.tif

The image shows a long, thin strip of tissue running down a mostly white background, with a few smaller fragments near the bottom. Its shape resembles a biopsy-like tissue sample, although the image does not tell us how it was collected. The tissue is mainly pink and red, with some darker purple and greyish areas.

At this magnification, I cannot clearly identify individual structures such as glomeruli or tubules. However, the tissue has a fine, grainy appearance, and some areas near the lower end look darker and more densely stained. These differences could be related to tissue thickness, folding or staining, but a closer examination would be needed to confirm this.

The TIFF metadata shows that the image is 1120 × 2508 pixels, with three 8-bit RGB channels and JPEG compression. It is stored in 240 × 240 pixel tiles. Python confirmed that the image has a uint8 data type, with observed pixel values ranging from 1 to 255.

### SkinOverview.tif

Unlike the kidney image, SkinOverview.tif shows an overview of the glass slide rather than only the tissue. There is a printed label along the left side, a green rectangle around the central tissue area, and dark borders with scattered colored speckles.

Three separate pink-purple tissue sections are visible near the middle of the slide. Some contain rounded, darker areas surrounded by lighter tissue. These features may represent different structures within the skin, but I would need a higher-resolution image before identifying them confidently.

A macro overview provides a low-resolution view of the entire slide. It helps show where the tissue is located, how many sections are present and which areas may be worth examining more closely. A detailed microscopic image, on the other hand, allows smaller structures and cellular features to be studied.

The main difference I noticed is that the skin image includes the slide label, edges and a marked rectangular region, while the kidney image mainly shows tissue against a white background. The skin tissue sections are relatively compact and lightly stained, whereas the kidney sample appears as a long, narrow strip with stronger pink-red staining. Their orientations are also different: the kidney image is tall, while the skin overview is wide.

The metadata shows that SkinOverview.tif is a 1600 × 634 pixel RGB image with 8-bit samples and JPEG compression. Python confirmed a uint8 data type and an observed intensity range of 0 to 255.

Another difference is how the two TIFF files store their image data. Kidney1.tif uses tiles, while SkinOverview.tif uses strips containing 16 rows each.

Strips organize image data into groups of rows, whereas tiles divide an image into rectangular blocks. A strip-based layout can be suitable for relatively small images that are usually read in full. Tiles are particularly useful for large images because they allow individual regions to be accessed without reading the entire image.

This may help explain why the macro overview uses strips while the kidney image uses tiles. However, the metadata does not tell us why the original software selected these particular storage arrangements.

### TMA2-v2.tif

The TMA2 image was different from the previous TIFF files because it contained two image directories within a single file. Using `tiffinfo`, I found that directory 0 had dimensions of 3102 × 3102 pixels, while directory 1 was 1551 × 1551 pixels. Both directories used JPEG compression, three 8-bit samples per pixel and YCbCr photometric interpretation.

I used Python to load the two directories separately. The first image was returned as a `uint8` array with a shape of `(3102, 3102, 3)` and pixel values ranging from 13 to 255. The second image had a shape of `(1551, 1551, 3)`, with values ranging from 0 to 255.

Both images showed a roughly circular tissue section in the middle, with many small spaces, irregular structures and darker stained areas. The background appeared unusually pink rather than white.

The two images looked very similar, but the second had half the width and height of the first. This suggests that directory 1 is a reduced-resolution representation of the same tissue section. It contains only one-quarter as many pixels as directory 0.

The unusually pink background raised a question about colour interpretation, which I investigated by converting the TIFF to RGBA.

### Checking the color interpretation

When I first displayed the TMA2 image using Python, the background appeared unusually pink. This was different from the mostly white backgrounds in the other tissue images.

The TIFF metadata showed that TMA2 used YCbCr rather than RGB color interpretation, so I investigated whether the pixel values were being displayed correctly.

I converted the original TIFF to RGBA using `tiff2rgba` and compared pixel values at the same locations. In the original image, the top-left pixel was `[242, 127, 127]`, while the converted image returned `[241, 243, 240, 255]`.

This suggests that the original Python reader returned YCbCr-like values that Matplotlib interpreted as RGB. The converted values indicate a nearly white background rather than a pink one.

The comparison demonstrates why checking image metadata is important. Even when an image loads successfully, its colors may be displayed incorrectly if the pixel values are interpreted using the wrong color representation.

The converted TIFF was successfully loaded in Python as a four-channel `uint8` image with dimensions of 3102 × 3102 pixels. Its observed pixel values ranged from 0 to 255. The additional channel represents alpha information.

The conversion preserved the image dimensions while changing the photometric interpretation from YCbCr to RGB with an alpha channel. The pixel comparison supports the explanation that the unusual pink appearance in the original display was caused by interpreting YCbCr-like values as RGB. The corrected image was saved separately so that both versions could be compared.

### Final visual comparison

After converting the TMA2 image from YCbCr to RGBA, the displayed colors changed considerably. The strong pink background disappeared and became almost white.

The corrected image shows a roughly circular tissue section containing many blue-stained structures, small brown or dark spots, and irregular clear spaces. These details were difficult to interpret in the original display because the colors were distorted.

The comparison showed me that successfully opening an image does not necessarily mean it is being displayed correctly. In this case, checking the TIFF metadata and comparing pixel values helped identify the problem. The corrected RGB representation is more suitable for visual examination, although the exact tissue type and staining method cannot be confirmed from the image alone.

##### DAPI fluorescence image

I loaded the DAPI image in Python and displayed it in grayscale. The image had a shape of `(1024, 1392)`, with unsigned 8-bit pixel values ranging from 3 to 255.

The image shows many bright, rounded and oval structures against a dark background. Since DAPI is commonly used to stain DNA, these structures are consistent with cell nuclei. Some appear clearly separated, while others are close together or overlap.

I also noticed differences in brightness. Some structures are quite faint, while others are much brighter. A few irregular areas are especially bright. The maximum intensity of 255 suggests that some pixels may be saturated, although further analysis would be needed to determine how widespread this is.

The image is stored as a single grayscale channel. Its intensity values can later be assigned to one color channel when constructing a combined fluorescence image.

The three images have identical dimensions, use unsigned 8-bit grayscale values, are LZW-compressed and are stored in strips of 128 rows.

##### FITC fluorescence image

I loaded the FITC image separately and displayed it in grayscale. The image had dimensions of 1392 × 1024 pixels, with unsigned 8-bit intensity values ranging from 0 to 255.

Compared with the DAPI image, the FITC image appeared much darker overall. Instead of many clearly visible oval structures, I noticed numerous small bright spots scattered across the image. There were also some faint larger structures and a brighter curved region around the centre and lower part.

Although both images came from the same field of view, the fluorescence patterns were different. DAPI mainly highlighted rounded structures consistent with nuclei, while the FITC channel showed a more scattered distribution of fluorescence.

The FITC image reached the maximum 8-bit intensity of 255, but this alone does not tell us how many pixels were saturated. The exact biological target of the FITC signal also cannot be determined from the image filename alone.

##### Acridine Orange fluorescence image

The Acridine Orange image was loaded as a single-channel `uint8` array with dimensions of 1024 × 1392 pixels. Its intensity values ranged from 0 to 255.

The image had a mostly dark background, with faint rounded structures and numerous small bright spots. I also noticed several brighter regions, particularly toward the left and centre of the field.

Compared with DAPI, the signal was less concentrated in clearly defined oval structures. It looked more similar to FITC, although some areas appeared more diffuse.

All three fluorescence images had identical dimensions and could therefore be combined into an RGB image without resizing.

### Combining the fluorescence channels into an RGB image

After examining the three grayscale fluorescence images separately, I combined them into a single RGB image using NumPy. All three images had the same dimensions of 1392 × 1024 pixels and were stored as unsigned 8-bit arrays, so no resizing or intensity conversion was needed.

I assigned Acridine Orange to the red channel, FITC to green and DAPI to blue. The resulting image had a shape of `(1024, 1392, 3)` and a data type of `uint8`.

The combined image made it easier to compare the different fluorescence patterns. The DAPI channel highlighted many rounded and oval structures in blue. The FITC channel contributed small green spots and several brighter regions, while Acridine Orange added red and magenta signals. Some structures appeared purple, cyan or almost white where signals from different channels overlapped.

One thing I noticed was that the three channels did not highlight exactly the same structures, even though they came from the same field of view. Viewing them together helped reveal where their signals were separate and where they overlapped.

The colors in the composite were assigned for visualization. They do not mean that the original grayscale images contained red, green or blue pixels.

### Kidney2_RGB2_20x.svs

I inspected `Kidney2_RGB2_20x.svs`, a whole-slide kidney image. Its full-resolution directory (directory 0) measures 7,967 × 39,056 pixels and uses 240 × 240 pixel tiles, JPEG compression and RGB photometric interpretation. The metadata reports a magnification of 20× and a pixel size of 0.4936 µm per pixel.

The file has six TIFF directories. Directory 0 contains the full-resolution image. Directory 1 is a small overview (156 × 768 pixels), while directories 2 and 3 contain smaller tiled versions (1,991 × 9,764 and 497 × 2,441 pixels). Directory 4 contains the slide label (660 × 675 pixels), and directory 5 contains a macro image (1,600 × 634 pixels). The full-resolution image and the two smaller tiled versions provide different levels of detail without requiring every view to be generated from the largest image.

I displayed directory 1 first. It showed a long, narrow tissue sample against a mostly light background, with some separated fragments. At this overview scale, the arrangement of the sample was clear, but individual microscopic structures were difficult to distinguish. The loaded overview had a shape of `(768, 156, 3)`, a `uint8` data type, and observed pixel values from 19 to 255.

### Reading a region from a tiled whole-slide image

To examine a small part of the full-resolution slide, I used `read_one_tile()` after selecting directory 0. I checked that the directory was tiled, then tested individual locations. The tile at `(1200, 2400)` was almost entirely light background, with pixel values from 243 to 246. Although the function worked, this location did not contain useful tissue detail.

I then tested `(2400, 25200)`. This tile showed stained kidney tissue with rounded and irregular tubule-like profiles, pale spaces and darker purple nuclei. Its pixel values ranged from 10 to 255. The difference between these two tiles showed why choosing the coordinates carefully matters.

After that, I used two nested loops to assemble a 3 × 3 block of neighbouring tiles. I checked the saved Python script and confirmed that the starting coordinates were `(2160, 24960)`, not `(1200, 2400)`. Each loop step moved 240 pixels horizontally or vertically, so the nine tiles covered X = 2160–2879 and Y = 24960–25679, using inclusive pixel coordinates. The tissue-containing tile at `(2400, 25200)` was in the centre of the block.

The combined image had a shape of `(720, 720, 3)` and a `uint8` data type. I saved it as `results/kidney_tile_region.png`. The image showed a larger continuous area of tissue, with no obvious gaps between neighbouring tiles.

This exercise helped me understand why tiled storage is useful for whole-slide images. I could inspect a small area by reading nine tiles rather than loading the full-resolution image. It also showed that a successful tile read does not guarantee a useful image: the selected coordinates might still fall on empty background.

**Figure files:** `results/kidney_wsi_overview.png`, `results/kidney_background_tile.png`, `results/kidney_tissue_tile_test.png`, and `results/kidney_tile_region.png`.


## Part 2 — Intensity transformations

#### Gamma correction of the washed-out aerial image

I started by examining `Fig0309(a)(washed_out_aerial_image).tif` from ImgSet2. Python returned a grayscale image with dimensions of 769 × 765 pixels and an unsigned 8-bit data type. The minimum and maximum pixel values were 0 and 255.

I applied gamma correction using the power-law transformation:

\[
s = 255(r/255)^\gamma
\]

For the first experiment, I used gamma = 0.5. I performed the calculation using NumPy, rounded the resulting values, and converted the corrected image back to `uint8`.

The mean intensity increased from 197.12 in the original image to 222.55 after correction. At row 100, column 100, the pixel intensity increased from 220 to 237. The image dimensions remained unchanged at 769 × 765 pixels, and the minimum and maximum intensities remained 0 and 255.

These results show that gamma = 0.5 increased the brightness of the image, particularly for intermediate intensity values. However, because the original image already had a relatively high mean intensity, increasing its brightness does not necessarily improve the visibility of its details.

I saved the corrected image as `aerial_gamma_05.png` and the side-by-side comparison as `aerial_gamma_comparison.png`.

#### Comparing gamma values of 0.5 and 2.0

After testing gamma = 0.5, I repeated the transformation using gamma = 2.0 on the same aerial image.

With gamma = 2.0, the mean intensity decreased from 197.12 to 158.95. The pixel at row 100, column 100 decreased from 220 to 190. In contrast, gamma = 0.5 increased the mean intensity to 222.55 and changed the same pixel to 237.

Both transformations preserved the image dimensions of 769 × 765 pixels, the `uint8` data type, and the minimum and maximum intensity values of 0 and 255.

These results demonstrate that gamma values below 1 increase intermediate pixel intensities, while gamma values above 1 decrease them. Gamma correction therefore changes the distribution of pixel brightness without changing the spatial dimensions of the image.

Since the original aerial image had a relatively high mean intensity, gamma = 2.0 reduced its overall brightness. However, the numerical results alone are not sufficient to determine which gamma value gives the best visual contrast. This requires examining the resulting images and their intensity distributions.
#### Histogram of the original aerial image

I calculated the intensity histogram of the original aerial image using NumPy. The image contained 588,285 pixels, and the sum of all histogram frequencies was also 588,285, confirming that every pixel was included.

The most frequent intensity was 213, which is a relatively light gray value on the 0–255 scale. This is consistent with the high mean intensity of 197.12 measured earlier.

Although the image contained pixel values ranging from 0 to 255, this did not mean that the intensities were evenly distributed. The histogram was useful for investigating how frequently different intensity values occurred and for understanding why the image appeared relatively bright.
#### Interpretation of the aerial image histogram

After plotting the histogram, I observed that the pixel intensities were not evenly distributed. Most of the larger frequencies occurred in the brighter part of the grayscale range, particularly between approximately 190 and 235.

The highest peak was at intensity 213, which agreed with the most frequent value calculated in Python. There were also smaller peaks at lower intensities, but these occurred less frequently.

This helps explain why the original image appeared washed out. Although its pixel values extended from 0 to 255, many pixels were concentrated in the brighter part of the range.

I also learned that knowing only the minimum and maximum intensities is not enough to describe image contrast. The histogram provides additional information about how the pixel values are distributed.
#### Piecewise-linear contrast stretching of the aerial image

I applied a piecewise-linear contrast transformation to the aerial image using an input intensity interval of 100 to 220. Values below 100 were mapped to 0, values above 220 were mapped to 255, and values between these limits were scaled linearly.

I implemented the transformation using nested loops, so that each pixel was processed individually. The calculated values were rounded before being stored in a new unsigned 8-bit image.

The mean intensity changed from 197.12 to approximately 200.00. At row 100, column 100, the original pixel intensity of 220 became 255. The output image retained the original dimensions of 769 × 765 pixels.

Although the mean intensity changed only slightly, the transformation redistributed pixel intensities by expanding the selected interval across the full grayscale range. This differs from gamma correction, which uses a power-law function.

One limitation of the method is that intensities outside the selected interval are clipped. Consequently, different original intensities can produce the same output value, causing some information to be lost.
#### Effect of clipping during contrast stretching

To investigate the effect of my selected intensity interval, I counted how many pixels in the original aerial image were below 100 or above 220.

I found that 25,784 pixels (4.38%) had intensities below 100, while 157,827 pixels (26.83%) had intensities above 220. Together, these accounted for 183,611 pixels, or approximately 31.21% of the image.

This showed that the interval of 100–220 excluded a substantial proportion of the original pixel intensities, especially at the brighter end of the range.

In the transformed image, pixels below 100 were assigned an intensity of 0, while those above 220 were assigned 255. Although this can increase the separation between intensities within the selected interval, it removes differences between values outside that interval.

I therefore concluded that the choice of stretching limits is important. A narrow interval may increase contrast in some regions while causing unnecessary clipping in others.
#### Comparison of original and contrast-stretched histograms

I compared the intensity histograms before and after applying piecewise-linear contrast stretching to the aerial image.

The original histogram showed a concentration of pixel intensities toward the brighter end of the grayscale range, with the highest frequency at intensity 213.

After stretching the interval from 100 to 220, the histogram changed considerably. The intermediate intensities were redistributed, while large peaks appeared at the endpoints.

The transformed image contained 25,784 pixels at intensity 0 and 169,069 pixels at intensity 255. This means approximately 28.74% of the pixels became completely white.

I initially counted 157,827 original pixels above intensity 220. The additional 11,242 white pixels came from pixels with an original intensity of exactly 220, which were also mapped to 255.

Both histograms contained 588,285 pixels in total, confirming that the transformation changed intensity values without changing the number of pixels.

This comparison showed that contrast stretching can expand a selected intensity interval, but it may also produce strong peaks at the endpoints when many original pixels are clipped.

#### Histogram equalization of the aerial image

I applied histogram equalization to the washed-out aerial image using its intensity histogram and cumulative distribution function (CDF).

The original image contained 588,285 pixels. I calculated the histogram using NumPy and then obtained the CDF by calculating the cumulative sum of the histogram frequencies.

I used the CDF to construct a lookup table containing 256 output intensity values. For example, an original intensity of 100 was mapped to 11, while intensity 213 was mapped to 154.

After applying the lookup table to the image, the mean intensity decreased from 197.12 to 128.83. The pixel at row 100, column 100 changed from 220 to 187. The image retained its original dimensions of 769 × 765 pixels and its unsigned 8-bit data type.

When I compared the two images, I noticed that the original appeared pale, with relatively weak differences between many surrounding areas. After equalization, the airport runway, roads, buildings and land boundaries became more clearly distinguishable.

The darker regions were more pronounced, and several fine details were easier to see. However, some textured areas also appeared more grainy.

This experiment showed that histogram equalization can improve the visibility of structures in an image whose intensities are concentrated toward one part of the grayscale range. Unlike gamma correction, histogram equalization determines its intensity mapping from the image's cumulative intensity distribution.

#### Comparison of original and equalized histograms

After applying histogram equalization, I compared the original and transformed intensity histograms.

The original histogram showed a strong concentration of pixels toward the brighter end of the grayscale range. The equalized histogram was spread more widely across the available intensity range, with a different distribution of peaks.

I also counted how many intensity levels were actually present in each image. The original image contained 149 occupied intensity levels, while the equalized image contained 129.

This initially surprised me because I expected histogram equalization to use more intensity levels. However, the transformation uses discrete output values, and different original intensities can be mapped to the same output value after rounding.

Both histograms contained 588,285 pixels in total, confirming that the transformation changed pixel intensities without changing the image dimensions.

The equalized histogram was not perfectly flat. This showed that histogram equalization does not guarantee an equal number of pixels at every intensity level, particularly when working with discrete 8-bit images.

The visual comparison also showed stronger differences between roads, buildings, land boundaries and other structures after equalization, although some textured regions appeared more grainy.

#### Performance comparison of lookup-table implementations

I compared two methods of applying the same histogram-equalization lookup table to the aerial image. The first method used NumPy array indexing, while the second used nested Python loops to process each pixel individually.

The NumPy method took approximately 0.00541 seconds, while the nested-loop method took approximately 1.10409 seconds. In this experiment, NumPy indexing was about 204 times faster.

I also compared the output arrays using `np.array_equal()`, which returned `True`. This confirmed that both methods produced identical pixel values.

The difference in execution time can be explained by the overhead of executing Python instructions for every pixel. NumPy handles array indexing using optimized operations, making it more efficient for this type of image transformation.

The timing results describe one execution on my computer. Repeating the experiment would be necessary to obtain a more reliable estimate of typical performance.

## Part 3 — Spatial filtering

### Comparison of averaging filters

I applied 3 × 3, 5 × 5 and 9 × 9 averaging filters to the 500 × 500 grayscale test-pattern image. Each interior output pixel was calculated as the mean of its surrounding neighborhood. I retained the original pixel values along the image borders, where a complete neighborhood was unavailable.

The 3 × 3 filter produced mild smoothing, while the 5 × 5 and 9 × 9 filters produced progressively stronger blurring. The small black squares and thin vertical lines became less distinct, and the edges of the letters became softer. The noisy rectangular regions also appeared smoother because local intensity variations were reduced.

The original mean intensity was 207.364732. The mean intensities after 3 × 3, 5 × 5 and 9 × 9 filtering were approximately 207.364778, 207.364749 and 207.364737, respectively.

Although the mean intensities remained nearly unchanged, the visual differences were substantial. This shows that averaging filters can reduce local variations and image sharpness without significantly changing the overall mean intensity.

**Figure:** `results/averaging_filter_comparison.png` — Original test pattern compared with 3 × 3, 5 × 5 and 9 × 9 averaging filters.

### First-order numerical derivatives and gradient magnitude

I calculated the horizontal and vertical first-order derivatives of the 500 × 500 grayscale test-pattern image using differences between neighboring pixels. I converted the image to floating-point values before subtraction to preserve negative differences.

The horizontal derivative highlighted vertical boundaries, particularly the sides of the squares and vertical lines. The vertical derivative emphasized horizontal boundaries, such as the upper and lower edges of the squares.

I combined both derivatives to calculate the gradient magnitude. This produced an edge image in which the boundaries of the squares, circles, letters and lines were visible together.

The maximum gradient magnitude was approximately 360.62, while the mean was approximately 14.17. The gradient magnitude could exceed 255 because it combined the squared horizontal and vertical derivatives.

The noisy regions also produced strong derivative responses. This showed that numerical derivatives are sensitive not only to object boundaries but also to noise.

I used zero values for the final column of the horizontal derivative and the final row of the vertical derivative, where the forward differences were not calculated.

**Figure:** `results/first_derivative_comparison.png` — Original image, horizontal derivative, vertical derivative and gradient magnitude.

### Laplacian sharpening of the moon image

I applied the four-neighbor Laplacian operator to the 540 × 466 grayscale moon image. I then sharpened the image by subtracting the Laplacian response from the original image.

The sharpened image showed more pronounced crater boundaries and surface details compared with the original. The Laplacian response emphasized rapid intensity changes, particularly around the moon's outline and crater edges.

The original mean intensity was approximately 42.6583, while the sharpened mean intensity was approximately 42.7664. The sharpened image was clipped to the valid 8-bit intensity range of 0–255.

Although sharpening improved the visibility of local details, the Laplacian can also amplify noise and produce overly strong edges. Therefore, stronger sharpening does not necessarily mean better image quality.

**Figure:** `results/moon_laplacian_sharpening.png` — Original moon, Laplacian response and sharpened moon.
### Unsharp masking of the moon image

I applied unsharp masking to the 540 × 466 grayscale moon image. First, I created a blurred image using a 5 × 5 averaging filter. I then subtracted the blurred image from the original to obtain the unsharp mask.

The mask contained both positive and negative values, ranging from approximately −51.12 to +59.72. Its mean was approximately zero.

I added the mask back to the original image using a sharpening strength of k = 1.0. The sharpened result showed more pronounced crater boundaries and surface texture than the original image.

The original mean intensity was approximately 42.6583, while the sharpened mean was approximately 42.5530 after clipping and conversion to 8-bit values.

Compared with Laplacian sharpening, unsharp masking enhances details using the difference between the original and a blurred image. Both methods can improve edge visibility, but they may also amplify noise.

**Figure:** `results/moon_unsharp_masking.png` — Original moon, blurred moon, unsharp mask and sharpened moon.

## Part 4 — Geometric transformations

### Translation and image scaling

I first examined the 64 × 64 grayscale image `Pattern64.tif`, which had an unsigned 8-bit data type and an intensity range of 0–247.

I translated the image 10 pixels to the right and 5 pixels downward using inverse mapping. The original pixel at row 0, column 0 had an intensity of 30, which appeared at row 5, column 10 in the translated image. Pixels without a valid source position were assigned zero.

I then enlarged the image by a factor of two using nearest-neighbor interpolation. The resulting image had dimensions of 128 × 128 pixels. Each source pixel was replicated into a 2 × 2 block.

### Bilinear interpolation

I also enlarged the image to 128 × 128 pixels using bilinear interpolation. Unlike nearest-neighbor interpolation, bilinear interpolation calculated weighted averages of neighboring pixel values.

For example, the interpolated intensity at output pixel (1,1) was 27.25, whereas the original pixel at (0,0) had an intensity of 30.

The bilinear result appeared smoother than the nearest-neighbor result, particularly around transitions between dark and bright regions. However, interpolation did not introduce additional information about the original scene.

**Figures:** `results/pattern_translation.png` and `results/pattern_interpolation_comparison.png`.

### Kidney Segmentation and Overlap Analysis

The glomeruli, tubule and peritubular capillary segmentation masks were examined using their TIFF metadata and class labels. The tubule and capillary masks were read at a lower-resolution image level matching the glomeruli mask dimensions of 7519 × 1764 pixels. The corresponding tissue labels were 3 for glomeruli, 1 for tubules and 3 for capillaries.

Using the supplied bounding boxes, glomerulus 4 contained 14,473 glomerular pixels, while glomerulus 5 contained 15,343. Their overlaps with tubules were 309 pixels (2.14%) and 214 pixels (1.39%), respectively. The overlaps with capillaries were 671 pixels (4.64%) and 864 pixels (5.63%), respectively.

The bounding box for glomerulus 3 contained no pixels labeled as glomeruli, although 153 pixels had the undefined value 255. Consequently, no reliable glomerular area or overlap percentage could be established for this region.

At the nominal resolution of 1 µm per pixel, the segmented areas of glomeruli 4 and 5 were estimated as 14,473 µm² and 15,343 µm². These measurements assume that the segmentation masks share the same spatial origin and alignment. This assumption was not independently verified, so the measurements should be interpreted as preliminary estimates.

### Multistep Image Enhancement — Example 3-43

The multistep image-enhancement procedure was applied to the 800 × 500 skeleton image. First, a Laplacian filter was used to identify intensity changes, and its result was combined with the original image to improve sharpness.

A Sobel gradient was then calculated to highlight skeletal edges. The gradient was smoothed using a 3 × 3 averaging filter to reduce local variations. The smoothed gradient was combined with the Laplacian-sharpened image to create an enhancement mask, which was subsequently added to the original image.

Finally, a power-law transformation with gamma = 0.5 was applied. The resulting image showed brighter skeletal structures and improved visibility of details compared with the original.

Floating-point arrays were used during the intermediate calculations to preserve negative values and intensities above 255. These values were clipped and converted to 8-bit where necessary for display.

The eight processing stages are presented in `skeleton_multistep_comparison.png`.

### Composite Affine Transformation

A composite affine transformation was applied to the 64 × 64 grayscale pattern image. The transformation combined scaling by a factor of 1.5, rotation by 30 degrees and translation by 10 pixels horizontally and 5 pixels vertically.

The individual transformation matrices were combined in the order M = T × R × S. The resulting matrix was verified by multiplying it by its inverse, which produced the identity matrix.

Inverse mapping and bilinear interpolation were used to generate a 128 × 128 output image. Of the 16,384 output pixels, 7,321 mapped inside the original image boundaries.

Black regions appeared where output coordinates mapped outside the source image. The experiment demonstrates how scaling, rotation and translation can be combined into a single affine transformation.

### Kidney Segmentation Overlap at Original WSI Resolution

The kidney segmentation masks were compared at their nominal 1 µm/pixel resolution and resampled to the original whole-slide image resolution of 0.4936 µm/pixel. Nearest-neighbor interpolation was used to preserve the discrete segmentation labels during coordinate transformation.

For glomerulus 4, the resampled glomerular area was 14,490.06 µm². The tubule overlap was 1,296 WSI pixels (315.76 µm²), representing 2.18% of the glomerular area. The peritubular capillary overlap was 2,789 WSI pixels (679.51 µm²), corresponding to 4.69%.

For glomerulus 5, the resampled glomerular area was 15,291.88 µm². Its tubule overlap was 872 WSI pixels (212.45 µm²), representing 1.39%, while the capillary overlap was 3,524 WSI pixels (858.59 µm²), representing 5.61%.

Glomerulus 3 contained no pixels labeled as glomeruli within its specified bounding box. Therefore, no reliable glomerular area or percentage overlap could be established for that region.

The WSI-grid results were close to the measurements obtained at 1 µm/pixel. Small differences arose from discrete nearest-neighbor sampling and pixel-boundary effects. These calculations assume that the segmentation masks share the same spatial origin and are correctly aligned. The alignment was not independently verified, so the results should be interpreted as estimates.