from libtiff import TIFF
import numpy as np

PIXEL_SIZE_WSI = 0.4936
WSI_PIXEL_AREA = PIXEL_SIZE_WSI ** 2
MASK_PIXEL_AREA = 1.0


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

regions = {
    3: (4398, 4563, 434, 586),
    4: (3779, 3996, 732, 950),
    5: (3473, 3660, 698, 880),
}

physical_boxes = {
    3: [8219.4272, 5512.5248, 8370.4688, 5676.4000],
    4: [8516.5744, 4893.5504, 8733.7584, 5108.7600],
    5: [8483.5032, 4587.5184, 8663.6672, 4772.6184],
}

test_row, test_col = regions[4][0], regions[4][2]
print("\nGlomerulus 4 start on the mask grid:", test_row, test_col)
print("Glomerulus 4 start on the WSI grid:", test_row / PIXEL_SIZE_WSI, test_col / PIXEL_SIZE_WSI)


def percent_difference(wsi_value, mask_value):
    if mask_value == 0:
        return "n/a"
    return f"{(wsi_value - mask_value) / mask_value:+.2%}"


for number, (r0, r1, c0, c1) in regions.items():
    low_glom = glom[r0:r1, c0:c1] == 3
    low_tub = tub[r0:r1, c0:c1] == 1
    low_ptc = ptc[r0:r1, c0:c1] == 3

    low_glom_area = np.count_nonzero(low_glom) * MASK_PIXEL_AREA
    low_tub_area = np.count_nonzero(low_glom & low_tub) * MASK_PIXEL_AREA
    low_ptc_area = np.count_nonzero(low_glom & low_ptc) * MASK_PIXEL_AREA

    wsi_r0 = int(np.ceil(r0 / PIXEL_SIZE_WSI))
    wsi_r1 = int(np.ceil(r1 / PIXEL_SIZE_WSI))
    wsi_c0 = int(np.ceil(c0 / PIXEL_SIZE_WSI))
    wsi_c1 = int(np.ceil(c1 / PIXEL_SIZE_WSI))

    wsi_rows = np.arange(wsi_r0, wsi_r1)
    wsi_cols = np.arange(wsi_c0, wsi_c1)

    src_rows = np.floor(wsi_rows * PIXEL_SIZE_WSI).astype(int)
    src_cols = np.floor(wsi_cols * PIXEL_SIZE_WSI).astype(int)
    src_rows = np.clip(src_rows, 0, glom.shape[0] - 1)
    src_cols = np.clip(src_cols, 0, glom.shape[1] - 1)

    region_glom = glom[np.ix_(src_rows, src_cols)]
    region_tub = tub[np.ix_(src_rows, src_cols)]
    region_ptc = ptc[np.ix_(src_rows, src_cols)]

    glomerulus_pixels = region_glom == 3
    tubule_pixels = region_tub == 1
    capillary_pixels = region_ptc == 3

    glom_pixels_wsi = np.count_nonzero(glomerulus_pixels)
    tubule_overlap = np.count_nonzero(glomerulus_pixels & tubule_pixels)
    capillary_overlap = np.count_nonzero(glomerulus_pixels & capillary_pixels)

    glom_area_um2 = glom_pixels_wsi * WSI_PIXEL_AREA
    tubule_area_um2 = tubule_overlap * WSI_PIXEL_AREA
    capillary_area_um2 = capillary_overlap * WSI_PIXEL_AREA

    x_min, y_min, x_max, y_max = physical_boxes[number]

    print(f"\nGlomerulus {number}")
    print("  Mask-grid box (rows, cols):", (r0, r1), (c0, c1))
    print("  WSI-grid box (rows, cols):", (wsi_r0, wsi_r1), (wsi_c0, wsi_c1))
    print("  WSI region shape:", region_glom.shape)
    print("  Box size from the supplied coordinates (um):",
          round(x_max - x_min, 2), "wide x", round(y_max - y_min, 2), "tall")
    print("  Box size on the WSI grid (um):",
          round(len(wsi_cols) * PIXEL_SIZE_WSI, 2), "wide x",
          round(len(wsi_rows) * PIXEL_SIZE_WSI, 2), "tall")

    print("  Glomerulus label-3 pixels (WSI grid):", glom_pixels_wsi)
    print("  Overlap with tubules (WSI pixels):", tubule_overlap)
    print("  Overlap with capillaries (WSI pixels):", capillary_overlap)

    print("  Glomerulus area (um^2):", round(glom_area_um2, 2),
          "| 1 um grid:", low_glom_area, "|", percent_difference(glom_area_um2, low_glom_area))
    print("  Tubule overlap area (um^2):", round(tubule_area_um2, 2),
          "| 1 um grid:", low_tub_area, "|", percent_difference(tubule_area_um2, low_tub_area))
    print("  Capillary overlap area (um^2):", round(capillary_area_um2, 2),
          "| 1 um grid:", low_ptc_area, "|", percent_difference(capillary_area_um2, low_ptc_area))

    if glom_pixels_wsi > 0:
        print(f"  Tubule overlap: {tubule_overlap / glom_pixels_wsi:.2%} of the glomerulus")
        print(f"  Capillary overlap: {capillary_overlap / glom_pixels_wsi:.2%} of the glomerulus")
    else:
        print("  No label-3 pixels in this box, so no overlap percentages.")