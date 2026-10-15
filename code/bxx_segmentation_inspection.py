from libtiff import TIFF
import numpy as np

folder = "data/BXX/BXX/"


def load_mask(filename):
    tiff_file = TIFF.open(folder + filename, mode="r")
    return tiff_file.read_image()


def inspect_mask(name, mask):
    print(name, "shape:", mask.shape)
    print(name, "dtype:", mask.dtype)
    print(name, "minimum:", np.min(mask))
    print(name, "maximum:", np.max(mask))
    print(name, "labels:", np.unique(mask))
    print()


glom = load_mask("BXX_GLOM.tif")
tub = load_mask("BXX_TUB.tif")
ptc = load_mask("BXX_PTC.tif")

inspect_mask("Glomeruli", glom)
inspect_mask("Tubules", tub)
inspect_mask("Peritubular capillaries", ptc)