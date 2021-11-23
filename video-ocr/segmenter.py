import os
import cv2
from segment_finder import VideoSegmentFinder
video_segment_finder = VideoSegmentFinder()

# Get the selected frames
print('Getting selected frames')
selected_frames_data = video_segment_finder.get_best_segment_frames('Downloads/9899a257681e440196a74f32afdf0f0f.mp4')
frame_nums = sorted(selected_frames_data.keys())
selected_frames = [selected_frames_data[i]["frame"] for i in frame_nums]

#print(selected_frames)

foldername = '9899a257681e440196a74f32afdf0f0f3'

if not os.path.exists(foldername):
    os.makedirs(foldername)
 

for i in range(0, len(selected_frames)):
    frame = selected_frames[i]

    #assign a name for our files 
    name = './'+foldername+'/frame' + str(i) + '.png'
    
    #assign our print statement
    print ('Extracting frames...' + name)
    cv2.imwrite(name, frame)