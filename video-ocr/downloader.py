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



url = 'https://www.youtube.com/watch?v=bPgIRk5C3jo'
file_md5sum = uuid.uuid4().hex

youtube = YouTube(url)
stream = youtube.streams.filter(adaptive=True).first()

vidpath = os.path.join(os.getcwd(),'Downloads')
print(vidpath)
stream.download(vidpath, file_md5sum)

file_md5sum = move_video_to(
    os.path.join(vidpath, file_md5sum),vidpath)

print(vidpath)
print(file_md5sum)
print('end')