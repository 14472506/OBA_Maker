from PIL import Image
import os

# Specify the directory containing the images
image_directory = 'base_images'

# Initialize variables to store max and min dimensions
max_width, max_height = 0, 0
min_width, min_height = float('inf'), float('inf')

# Iterate through each file in the directory
for filename in os.listdir(image_directory):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')):
        # Construct the full file path
        file_path = os.path.join(image_directory, filename)
        
        # Open the image and get its dimensions
        with Image.open(file_path) as img:
            width, height = img.size
            
            # Update max dimensions
            if width > max_width:
                max_width = width
            if height > max_height:
                max_height = height
            
            # Update min dimensions
            if width < min_width:
                min_width = width
            if height < min_height:
                min_height = height

# Print the results
print(f"Maximum dimensions: {max_width}x{max_height}")
print(f"Minimum dimensions: {min_width}x{min_height}")
