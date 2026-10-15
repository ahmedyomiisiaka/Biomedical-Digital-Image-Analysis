import numpy as np

pixel = 64
gamma = 2.0

new_intensity = 255 * (pixel / 255) ** gamma

print("Original intensity:", pixel)
print("New intensity:", new_intensity)