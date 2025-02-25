import os
import json
import random
import numpy as np
from PIL import Image

# This code is unoptimized. Could be optimized for faster generation.

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

    # Set 224x224 - THIS IS IMPORTANT
    image = Image.new('RGB', (224, 224), color_rgb)
    image_filename = f"color_img_{i + 1}.png"
    image_path = os.path.join(image_dir, image_filename)

    # Save the image
    image.save(image_path)

    # Convert image to NumPy array with shape (3, 224, 224)
    image_array = np.array(image).transpose((2, 0, 1))  # Shape: (3, 224, 224)

    # ✅ Normalize pixel values to the range [0, 1]
    normalized_image_array = image_array / 255.0

    # Save normalized pixel values
    pixel_values_filename = f"pixel_values_{i + 1}.json"
    pixel_values_path = os.path.join(pixel_values_dir, pixel_values_filename)

    with open(pixel_values_path, 'w') as pixel_file:
        json.dump(normalized_image_array.tolist(), pixel_file)

    # ✅ Prepare JSON entry with 'labels' structure
    image_data = {
        "index_num": i + 1,
        "file_link": f"color_img/{image_filename}",
        "pixel_values_link": f"pixel_values/{pixel_values_filename}",
        "labels": {
            "description": f"This is a solid {color_name.lower()} color image.",
            "QA_pairs": [
                {"question": f"Is this color {color_name.lower()}?", "answer": "Yes"},
                {"question": f"Is this color some other color?", "answer": "No"}
            ]
        }
    }
    image_data_list.append(image_data)

    # Debug output
    print(f"Generated image {i + 1}: {color_name} saved as {image_filename}")

# ✅ Save JSON file
json_output_path = os.path.join(output_dir, "color_images_metadata.json")
with open(json_output_path, 'w') as json_file:
    json.dump(image_data_list, json_file, indent=4)

print(f"100 solid color images and metadata JSON saved in '{output_dir}'")
