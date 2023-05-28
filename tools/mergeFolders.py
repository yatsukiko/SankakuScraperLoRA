import os
import sys
import shutil

# Check if correct number of arguments provided
if len(sys.argv) != 3:
    print("Usage: python merge_folders.py <folder1> <folder2>")
    sys.exit(1)

# Get folder paths from command line arguments
folder1 = sys.argv[1]
folder2 = sys.argv[2]

# Create merged folder if it doesn't exist
merged_folder = "merged"
if not os.path.exists(merged_folder):
    os.makedirs(merged_folder)

# Function to copy and rename files
def copy_and_rename(src, dst, count):
    base_name = os.path.basename(src)
    file_name, file_ext = os.path.splitext(base_name)
    new_name = str(count) + file_ext
    txt_name = str(count) + ".txt"
    shutil.copy2(src, os.path.join(dst, new_name))
    
    # Find corresponding text file using image file name
    txt_src = os.path.join(os.path.dirname(src), file_name + ".txt")
    txt_dst = os.path.join(dst, txt_name)
    shutil.copy2(txt_src, txt_dst)

# Merge folder1
for count, file_name in enumerate(os.listdir(folder1), start=1):
    if file_name.endswith(".jpg") or file_name.endswith(".png"):
        src = os.path.join(folder1, file_name)
        copy_and_rename(src, merged_folder, count)

# Merge folder2
for count, file_name in enumerate(os.listdir(folder2), start=count+1):
    if file_name.endswith(".jpg") or file_name.endswith(".png"):
        src = os.path.join(folder2, file_name)
        copy_and_rename(src, merged_folder, count)

print("Merging completed successfully.")
