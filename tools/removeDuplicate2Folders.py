import os
import cv2
import numpy as np
from skimage.metrics import structural_similarity as compare_ssim
import sys

def get_image_similarity(img1, img2):
    """Calculates and returns the Structural Similarity Index (SSIM) between two images."""
    # Resize images to a specified size (e.g., 256x256) for comparison
    img1 = cv2.resize(img1, (256, 256))
    img2 = cv2.resize(img2, (256, 256))
    img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    score = compare_ssim(img1_gray, img2_gray)
    return score

def find_and_remove_duplicates(folder1, folder2, similarity_threshold=0.98):
    """Scans two folders for images and removes 1:1 duplicates based on SSIM similarity threshold."""
    # Get list of files in folders
    files1 = os.listdir(folder1)
    files2 = os.listdir(folder2)

    for file1 in files1:
        img1_path = os.path.join(folder1, file1)
        if not os.path.isfile(img1_path) or not any(img1_path.endswith(ext) for ext in ('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
            continue
        img1 = cv2.imread(img1_path)

        for file2 in files2:
            img2_path = os.path.join(folder2, file2)
            if not os.path.isfile(img2_path) or not any(img2_path.endswith(ext) for ext in ('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
                continue
            img2 = cv2.imread(img2_path)

            similarity = get_image_similarity(img1, img2)

            if similarity >= similarity_threshold:
                print(f'Removing duplicate: {file1} and {file2}')
                os.remove(img2_path)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python script.py folder1 folder2')
        sys.exit(1)

    folder1 = sys.argv[1]
    folder2 = sys.argv[2]
    similarity_threshold = 0.98

    find_and_remove_duplicates(folder1, folder2, similarity_threshold)
