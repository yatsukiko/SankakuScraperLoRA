import os
import cv2
import sys
import shutil
from PIL import Image
from torchvision.transforms import Resize
from SSIM_PIL import compare_ssim

def compare_images(image1_path, image2_path):
    # Load the images
    image1 = Image.open(image1_path)
    image2 = Image.open(image2_path)

    # Convert both images to RGB color mode
    image1 = image1.convert('RGB')
    image2 = image2.convert('RGB')

    # Resize the images to 256x256 pixels
    size = (256, 256)
    resize_transform = Resize(size)
    image1 = resize_transform(image1)
    image2 = resize_transform(image2)

    # Compare the resized images using SSIM
    similarity = compare_ssim(image1, image2)
    return similarity

def move_file(source_path, destination_dir):
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)
    shutil.move(source_path, os.path.join(destination_dir, os.path.basename(source_path)))

def find_duplicates(source_dir, threshold):
    image_files = [f for f in os.listdir(source_dir) if f.lower().endswith(('.jpg', '.png'))]
    num_images = len(image_files)
    duplicate_files = []
    processed_count = 0
    print("Comparing images for duplicates...")
    for i in range(num_images):
        image1_path = os.path.join(source_dir, image_files[i])
        if not os.path.exists(image1_path):
            print("File not found: {}".format(image1_path))
            continue
        for j in range(i+1, num_images):
            image2_path = os.path.join(source_dir, image_files[j])
            if not os.path.exists(image2_path):
                print("File not found: {}".format(image2_path))
                continue
            similarity = compare_images(image1_path, image2_path)
            if similarity > threshold:
                duplicate_files.append(image_files[i])
                duplicate_files.append(image_files[j])
                move_file(image2_path, "rejected")
                print("Duplicate found: {} and {}. Similarity: {:.2f}".format(image_files[i], image_files[j], similarity))
                break
            processed_count += 1
    print("Image comparison for duplicates completed.")
    return duplicate_files

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python script_name.py source_directory threshold")
        sys.exit(1)
    source_dir = sys.argv[1]
    threshold = 0.98
    if len(sys.argv) > 2:
        threshold = float(sys.argv[2])
    find_duplicates(source_dir, threshold)