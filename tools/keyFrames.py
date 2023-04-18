import cv2
import os
import shutil
import sys

def extract_key_frames(videos_dir):
    # Get list of files in the directory
    files = os.listdir(videos_dir)

    # Filter video files
    video_files = [f for f in files if f.lower().endswith(('.mp4', '.avi', '.mkv', '.mov', 'webm'))]

    # Get video properties for each video file
    for video_file in video_files:
        video_path = os.path.join(videos_dir, video_file)
        cap = cv2.VideoCapture(video_path)
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        video_duration = frame_count // fps

        # Calculate interval between key frames
        num_key_frames = 3  # Number of key frames to extract
        interval = video_duration // (num_key_frames + 1)

        # Loop through frames and extract key frames
        key_frames = []
        for i in range(1, num_key_frames + 1):
            # Calculate target frame number
            target_frame = int(interval * i * fps)
            # Set video capture to target frame
            cap.set(cv2.CAP_PROP_POS_FRAMES, target_frame)
            # Read frame
            ret, frame = cap.read()
            if ret:
                key_frames.append(frame)

        # Save key frames as images
        for i, frame in enumerate(key_frames):
            output_name = f'{os.path.splitext(video_file)[0]}_{i+1}.png'
            output_path = os.path.join(videos_dir, output_name)
            cv2.imwrite(output_path, frame)

            # Copy .txt file
            txt_file = os.path.splitext(video_file)[0] + '.txt'
            txt_file_path = os.path.join(videos_dir, txt_file)
            if os.path.exists(txt_file_path):
                txt_output_name = f'{os.path.splitext(video_file)[0]}_{i+1}.txt'
                txt_output_path = os.path.join(videos_dir, txt_output_name)
                shutil.copy(txt_file_path, txt_output_path)

        # Release video capture
        cap.release()

        # Delete original video file
        os.remove(video_path)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script_name.py videos_dir")
    else:
        videos_dir = sys.argv[1]
        extract_key_frames(videos_dir)
