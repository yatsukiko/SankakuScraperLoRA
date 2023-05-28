import os
import cv2
import shutil

def compare_images(image1_path, image2_path):
    image1 = cv2.imread(image1_path, cv2.IMREAD_GRAYSCALE)
    image2 = cv2.imread(image2_path, cv2.IMREAD_GRAYSCALE)
    orb = cv2.ORB_create()
    keypoints1, descriptors1 = orb.detectAndCompute(image1, None)
    keypoints2, descriptors2 = orb.detectAndCompute(image2, None)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(descriptors1, descriptors2)
    similar_regions = [i for i in matches if i.distance < 70]
    return len(similar_regions) > 0

def move_files(source_dir, destination_dir, file_list):
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)
    for file in file_list:
        shutil.move(os.path.join(source_dir, file), os.path.join(destination_dir, file))

def find_duplicates(source_dir, threshold):
    image_files = [f for f in os.listdir(source_dir) if f.lower().endswith(('.jpg', '.png'))]
    num_images = len(image_files)
    duplicate_files = []
    processed_count = 0
    print("Comparing images for duplicates...")
    for i in range(num_images):
        for j in range(i+1, num_images):
            image1_path = os.path.join(source_dir, image_files[i])
            image2_path = os.path.join(source_dir, image_files[j])
            print(f"Processing: {image_files[i]} vs {image_files[j]}")
            if compare_images(image1_path, image2_path) >= threshold:
                duplicate_files.append(image_files[i])
                duplicate_files.append(image_files[j])
        processed_count += 1
        print(f"Processed {processed_count}/{num_images} images...", end='\r')
    print("Comparison complete.")
    duplicate_files = list(set(duplicate_files)) # remove duplicates in duplicate_files list
    move_files(source_dir, os.path.join(source_dir, 'rejected'), duplicate_files)
    for file in duplicate_files:
        txt_file = file.split('.')[0] + '.txt'
        if os.path.exists(os.path.join(source_dir, txt_file)):
            shutil.move(os.path.join(source_dir, txt_file), os.path.join(source_dir, 'rejected', txt_file))
    print("Moved duplicate files to 'rejected' folder.")
    print(f"Similarity threshold: {threshold}")

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Usage: python duplicate_checker.py <source_dir>")
    else:
        source_dir = sys.argv[1]
        threshold = 0.98
        find_duplicates(source_dir, threshold)