import os
import cv2
from segment_finder0 import VideoSegmentFinder
video_segment_finder = VideoSegmentFinder()

# Get the selected frames
print('Getting selected frames')
selected_frames_data = video_segment_finder.get_best_segment_frames('Downloads/fd576ad482d94cff8c0ae7dd60a403e9.mp4')
frame_nums = sorted(selected_frames_data.keys())
selected_frames = [selected_frames_data[i]["frame"] for i in frame_nums]

#print(selected_frames)


if not os.path.exists('image_frames2'):
    os.makedirs('image_frames2')
 

for i in range(0, len(selected_frames)):
    frame = selected_frames[i]

    #assign a name for our files 
    name = './image_frames2/frame' + str(i) + '.png'
    
    #assign our print statement
    print ('Extracting frames...' + name)
    cv2.imwrite(name, frame)