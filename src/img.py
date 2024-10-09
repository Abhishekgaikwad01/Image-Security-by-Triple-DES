from PIL import Image

# Create a new image with RGB mode (no alpha channel) and size 100x100
image = Image.new("RGB", (100, 100))

# Load the pixels for editing
pixels = image.load()

# Set the left half to red and the right half to blue
for i in range(100):
    for j in range(100):
        if i < 50:  # Left half (Red)
            pixels[i, j] = (255, 0, 0)  # RGB for red
        else:  # Right half (Blue)
            pixels[i, j] = (0, 0, 255)  # RGB for blue

# Save the image
image.save('simple_image.png')
print("Simple image created and saved as 'simple_image.png'")
