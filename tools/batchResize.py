import os
import sys
from PIL import Image

# Check if source folder is provided as a command-line argument
if len(sys.argv) < 2:
    print("Please provide the source folder as a command-line argument.")
    sys.exit(1)

# Get the source folder path from command-line argument
src_folder = sys.argv[1]

# Check if source folder exists
if not os.path.exists(src_folder):
    print("Source folder does not exist.")
    sys.exit(1)

# Loop through all files in the source folder
for filename in os.listdir(src_folder):
    # Get the file path
    file_path = os.path.join(src_folder, filename)

    # Check if the file is an image
    if file_path.endswith(('.jpg', '.jpeg', '.png', '.gif')):
        try:
            # Open the image using Pillow
            with Image.open(file_path) as img:
                # Resize the image to 768x768
                img = img.resize((768, 768))
                # Save the resized image back to the same file
                img.save(file_path)
                print(f"Resized {filename} to 768x768.")
        except Exception as e:
            print(f"Failed to resize {filename}: {e}")
    else:
        print(f"Skipping {filename} as it is not an image.")
