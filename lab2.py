# -*- coding: utf-8 -*-
"""
Created on Sun Aug  4 20:22:46 2024

@author: pujal
"""

#Lab Task 1: Setup and Basic Extraction
import subprocess
import json
import os
def get_frame_info(video_path):
    cmd = [
        'ffprobe',
        '-v', 'error',
        '-select_streams', 'v:0',
        '-show_entries', 'frame=pict_type',
        '-of', 'json',
        video_path
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return json.loads(result.stdout)
video_path = r"C:\Users\pujal\Downloads\image&video_analytics\8632511-uhd_2160_3840_30fps.mp4"
frame_info = get_frame_info(video_path)

#Lab Task 2: Frame Type Analysis
#Count the number of I, P, and B frames and calculate their percentages:
frame_types = [frame['pict_type'] for frame in frame_info['frames']]
frame_counts = {frame_type: frame_types.count(frame_type) for frame_type in set(frame_types)}
total_frames = sum(frame_counts.values())
frame_percentages = {frame_type: (count / total_frames) * 100 for frame_type, count in frame_counts.items()}
print('Frame Counts:', frame_counts)
print('Frame Percentages:', frame_percentages)
#Analyze Frame Distribution:
import matplotlib.pyplot as plt
def plot_frame_distribution(frame_counts):
    labels = frame_counts.keys()
    sizes = frame_counts.values()
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.title('Frame Type Distribution - Pie Chart')
    plt.subplot(1, 2, 2)
    plt.bar(labels, sizes, color=['red', 'blue', 'green'])
    plt.xlabel('Frame Types')
    plt.ylabel('Counts')
    plt.title('Frame Type Distribution - Bar Graph')
    plt.tight_layout()
    plt.show()
plot_frame_distribution(frame_counts)

#Lab Task 3: Visualizing Frames
def extract_frames(video_path, output_dir, frame_types):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    for frame_type in frame_types:
        print(f"Extracting {frame_type} frames...")
        result = subprocess.run([
            'ffmpeg',
            '-i', video_path,
            '-vf', f'select=eq(pict_type\\,{frame_type})',
            '-vsync', 'vfr',
            '-f', 'image2',
            f'{output_dir}/{frame_type}_frame_%04d.jpg'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        if result.returncode != 0:
            print(f"Error extracting {frame_type} frames:\n{result.stderr}")
        else:
            print(f"{frame_type} frames extracted successfully.")

video_path = 'C:\\Users\\pujal\\Downloads\\image&video_analytics\\8632511-uhd_2160_3840_30fps.mp4'  # Replace with your video file path
output_dir = 'frames'
frame_types = ['I', 'P', 'B']
extract_frames(video_path, output_dir, frame_types)
from PIL import Image
def display_frames(frame_dir, frame_types):
    for frame_type in frame_types:
        frame_files = sorted([f for f in os.listdir(frame_dir) if f.startswith(frame_type)])
        for frame_file in frame_files[:5]:  # Display first 5 frames
            frame_path = os.path.join(frame_dir, frame_file)
            img = Image.open(frame_path)
            img.show()
display_frames('frames', frame_types)


#Lab Task 4: Frame Compression Analysis
#Calculate Frame Sizes
def calculate_frame_sizes(frame_dir, frame_types):
    frame_sizes = {frame_type: [] for frame_type in frame_types}
    for frame_type in frame_types:
        frame_files = sorted([f for f in os.listdir(frame_dir) if f.startswith(frame_type)])
        for frame_file in frame_files:
            frame_path = os.path.join(frame_dir, frame_file)
            frame_sizes[frame_type].append(os.path.getsize(frame_path))
    return frame_sizes

frame_sizes = calculate_frame_sizes('frames', frame_types)
# Calculate average sizes with a check for empty lists
average_sizes = {frame_type: (sum(sizes) / len(sizes) if sizes else 0) for frame_type, sizes in frame_sizes.items()}
print('Average Frame Sizes:', average_sizes)

#Lab Task 5: Advanced Frame Extraction
def reconstruct_video_from_i_frames(frame_dir, output_video):
    frame_files = sorted([os.path.join(frame_dir, f) for f in os.listdir(frame_dir) if f.endswith('.jpg')])
    subprocess.run([
        'ffmpeg',
        '-framerate', '1',  # Adjust frame rate as needed
        '-i', f'{frame_dir}/i_frame_%04d.jpg',
        '-c:v', 'libx264',
        '-r', '30',  # Set output frame rate
        '-pix_fmt', 'yuv420p',
        output_video
    ])
reconstruct_video_from_i_frames('frames', 'reconstructed_video.mp4')
