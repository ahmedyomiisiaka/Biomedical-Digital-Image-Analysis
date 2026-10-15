pixel = 180
low = 100
high = 220

if pixel < low:
    new_intensity = 0
elif pixel > high:
    new_intensity = 255
else:
    new_intensity = 255 * (pixel - low) / (high - low)

print("Original intensity:", pixel)
print("New intensity:", new_intensity)