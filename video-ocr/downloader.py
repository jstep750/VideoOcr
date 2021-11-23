import os
import uuid

from pytube import YouTube

def move_video_to(internal_video_path, destination_dir):
    
    # Get the Video's MD5 sum and ensure that it does not exist already
    video_md5sum = internal_video_path
    expected_video_path = os.path.join(destination_dir, video_md5sum + ".mp4")
    if not os.path.exists(destination_dir):     # create destination_dir
        os.makedirs(destination_dir)
    if not os.path.exists(expected_video_path):     # move file if not exists on destination
        os.rename(internal_video_path, expected_video_path)
    else:
        print("File with md5sum '{}' already exists on destination folder"
                      .format(video_md5sum))
    return video_md5sum



input_url = str('https://www.youtube.com/watch?v=ExaatgwYqfU')
# filename (for unique filename)
file_md5sum = uuid.uuid4().hex
file_name = file_md5sum
youtube = YouTube(input_url)

stream = youtube.streams.filter(adaptive=True, file_extension='mp4', only_video=True).first()

vidpath = os.path.join(os.getcwd(),'Downloads')
# vidpath = './Downloads'

if not os.path.exists(vidpath):     # create destination_dir
    os.makedirs(vidpath)

stream.download(vidpath, file_md5sum)

file_md5sum = move_video_to(
    os.path.join(vidpath, file_md5sum),vidpath)

print(file_name, end='')