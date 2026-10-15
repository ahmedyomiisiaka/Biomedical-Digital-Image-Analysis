from libtiff import TIFF
import numpy as np


def read_mask(path, directory=None):
    f = TIFF.open(path, mode="r")
    if directory is not None:
        f.SetDirectory(directory)
    return f.read_image()


tub = read_mask("data/BXX/BXX/BXX_TUB.tif", 2)
ptc = read_mask("data/BXX/BXX/BXX_PTC.tif", 2)
glom = read_mask("data/BXX/BXX/BXX_GLOM.tif")

print("Tubule mask shape:", tub.shape)
print("Capillary mask shape:", ptc.shape)
print("Glomeruli mask shape:", glom.shape)

same_shape = glom.shape == tub.shape == ptc.shape
print("All masks have the same shape:", same_shape)

if not same_shape:
    raise SystemExit("Shapes differ, so the same crop coordinates would not line up. Stopping.")

for name, mask in [("Glomeruli", glom), ("Tubule", tub), ("Capillary", ptc)]:
    values, counts = np.unique(mask, return_counts=True)
    print(f"\n{name} mask labels:")
    for v, c in zip(values, counts):
        print(f"  value {v}: {c} pixels")

regions = {
    3: (4398, 4563, 434, 586),
    4: (3779, 3996, 732, 950),
    5: (3473, 3660, 698, 880),
}

for number, (row_start, row_end, col_start, col_end) in regions.items():
    region_glom = glom[row_start:row_end, col_start:col_end]
    region_tub = tub[row_start:row_end, col_start:col_end]
    region_ptc = ptc[row_start:row_end, col_start:col_end]

    print(f"\nGlomerulus {number}")
    print("  Region shape:", region_glom.shape)
    print("  Glomerulus region labels:", np.unique(region_glom))
    print("  Pixels labeled 3:", np.count_nonzero(region_glom == 3))
    print("  Pixels labeled 255:", np.count_nonzero(region_glom == 255))
    print("  Tubule region labels:", np.unique(region_tub))
    print("  Capillary region labels:", np.unique(region_ptc))

    glomerulus_pixels = region_glom == 3
    tubule_pixels = region_tub == 1
    capillary_pixels = region_ptc == 3

    glom_area = np.count_nonzero(glomerulus_pixels)
    tubule_overlap = np.count_nonzero(glomerulus_pixels & tubule_pixels)
    capillary_overlap = np.count_nonzero(glomerulus_pixels & capillary_pixels)

    print("  Glomerulus label-3 pixels:", glom_area)
    print("  Estimated area (square micrometers):", glom_area * 1.0)
    print("  Overlap with tubules (pixels):", tubule_overlap)
    print("  Overlap with capillaries (pixels):", capillary_overlap)

    if glom_area > 0:
        print(f"  Tubule overlap: {tubule_overlap / glom_area:.2%} of the glomerulus")
        print(f"  Capillary overlap: {capillary_overlap / glom_area:.2%} of the glomerulus")
    else:
        print("  No label-3 pixels here, so no overlap percentages.")

    pixels_255 = region_glom == 255
    if np.count_nonzero(pixels_255) > 0:
        print("  [reference] 255 pixels & tubule:", np.count_nonzero(pixels_255 & tubule_pixels))
        print("  [reference] 255 pixels & capillary:", np.count_nonzero(pixels_255 & capillary_pixels))