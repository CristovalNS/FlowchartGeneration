import os
import json
import random
import numpy as np
from PIL import Image

# Directory to save images
output_dir = "model_input_test"
image_dir = os.path.join(output_dir, "color_img")
pixel_values_dir = os.path.join(output_dir, "pixel_values")

os.makedirs(image_dir, exist_ok=True)
os.makedirs(pixel_values_dir, exist_ok=True)

# List of color names and their RGB values
colors = {
    "Red": (255, 0, 0),
    "Green": (0, 255, 0),
    "Blue": (0, 0, 255),
    "Yellow": (255, 255, 0),
    "Cyan": (0, 255, 255),
    "Magenta": (255, 0, 255),
    "White": (255, 255, 255),
    "Black": (0, 0, 0),
    "Gray": (128, 128, 128),
    "Orange": (255, 165, 0),
    "Purple": (128, 0, 128),
    "Pink": (255, 192, 203),
    "Brown": (165, 42, 42),
    "Lime": (0, 255, 0),
    "Turquoise": (64, 224, 208)
}

# JSON data list
image_data_list = []

# Generate 100 solid color images
for i in range(100):
    # Randomly select a color
    color_name, color_rgb = random.choice(list(colors.items()))

    # Create a 214x214 image with the selected color
    image = Image.new('RGB', (214, 214), color_rgb)
    image_filename = f"color_img_{i + 1}.png"
    image_path = os.path.join(image_dir, image_filename)

    # Save the image
    image.save(image_path)

    # Convert image to NumPy array with shape (3, 214, 214)
    image_array = np.array(image).transpose((2, 0, 1))  # Transpose to (3, 214, 214)
    pixel_values_filename = f"pixel_values_{i + 1}.json"
    pixel_values_path = os.path.join(pixel_values_dir, pixel_values_filename)

    # Save pixel values to separate JSON file
    with open(pixel_values_path, 'w') as pixel_file:
        json.dump(image_array.tolist(), pixel_file)

    # Prepare JSON entry
    image_data = {
        "index_num": i + 1,
        "description": f"This is a solid {color_name.lower()} color image.",
        "file_link": f"model_input_test/color_img/{image_filename}",
        "pixel_values_link": f"model_input_test/pixel_values/{pixel_values_filename}",
        "QA_pairs": [
            {"question": f"Is this color {color_name.lower()}?", "answer": "Yes"},
            {"question": f"Is this color some other color?", "answer": "No"}
        ]
    }
    image_data_list.append(image_data)

    # Debug output
    print(f"Generated image {i + 1}: {color_name} saved as {image_filename}")

# Save JSON file
json_output_path = os.path.join(output_dir, "color_images_metadata.json")
with open(json_output_path, 'w') as json_file:
    json.dump(image_data_list, json_file, indent=4)

print(f"100 solid color images and metadata JSON saved in '{output_dir}'")
