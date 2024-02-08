from PIL import Image
import os

# Directory paths
source_directory = 'background_images'
output_directory = 'processed_background_images'

# Desired output dimensions and aspect ratio
output_width, output_height = 1920, 1080
aspect_ratio = output_width / output_height

# Process each image in the directory
for filename in os.listdir(source_directory):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')):
        file_path = os.path.join(source_directory, filename)
        
        with Image.open(file_path) as img:
            width, height = img.size

            # Ensure the image is wider than it is tall
            if width < height:
                img = img.rotate(90, expand=True)
                width, height = height, width  # Swap the dimensions for further processing

            # Calculate the largest possible crop dimensions with a 16:9 aspect ratio
            crop_height = height
            crop_width = crop_height * aspect_ratio
            if crop_width > width:
                # If the calculated width exceeds the image's width, adjust the height instead
                crop_width = width
                crop_height = crop_width / aspect_ratio

            # Calculate the crop area
            left = (width - crop_width) / 2
            top = (height - crop_height) / 2
            right = (width + crop_width) / 2
            bottom = (height + crop_height) / 2

            # Crop and resize the image
            img_cropped = img.crop((left, top, right, bottom))
            img_resized = img_cropped.resize((output_width, output_height), Image.ANTIALIAS)

            # Save the processed image
            output_path = os.path.join(output_directory, filename)
            img_resized.save(output_path)
