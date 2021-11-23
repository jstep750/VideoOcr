from collections import deque
import numpy as np
import cv2

def cal_time_to_frame(time, fps):
    frame_number = (time * fps)
    # fps는 flaot값으로 나오기 때문에 float값 상태에서 곱해준 뒤, 반올림을 해야 가장 근접한 프레임이 나온다.
    return round(frame_number)

class PastFrameChangesTracker:
    """ A class that keeps track of changes from previous frames """

    def __init__(self):
        self.prev_frame_changes = [False, False, False, False, False]

    def are_previous_frames_stable(self):
        """Checks if all previous frames had no changes

        Returns
        -------
        is_stable : boolean
            True if all past frames had no changes; else False
        """
        return sum([1 if x else 0 for x in self.prev_frame_changes]) == 0

    def add_frame_change(self, has_changed):
        """Adds a change to the tracker
        If there are more than 5 items in the tracker, it will evict the oldest frame change

        Parameters
        ----------
        has_changed : boolean
            True if there was a change with the current frame vs the past frame; else False

        Returns
        -------
        is_stable : boolean
            True if all past frames had no changes; else False
        """
        self.prev_frame_changes.append(has_changed)

        if len(self.prev_frame_changes) > 5:
            self.prev_frame_changes.pop(0)




class VideoSegmentFinder:
    """A class responsible for finding a list of best possible video segments
    A good video segment (a, t1, t2) is when image a is best explained when watching the video from time t1 to t2

    Attributes
    ----------
    threshold : int
        Is the min. difference between the color of two images on one pixel location for it to be distinct
    min_change : int
        Is the min. number of pixel changes between two adjacent video frames for the two to be considered distinct
    """

    def __init__(self, threshold=20, min_change=7000 , max_change=20000):
        self.threshold = threshold
        self.min_change = min_change
        self.max_change = max_change

    def get_best_segment_frames(self, video_file):
        ''' Finds a list of best possible video segments 
        It returns a map, where the key is the frame number, and the value is the frame data

        The frame data is of this format:
        {
            "timestamp": <the timestamp of the current frame>,
            "frame": <the current frame>,
            "next_frame": <the next frame>,
            "mask": <difference between current and next frame>,
            "num_pixels_changed": <number of pixel changes>,
        }

        The video segment can be obtained by two adjacent frame data, f1, f2 where:
            a = f2.frame
            t1 = f1.timestamp
            t2 = f2.timestamp

        Returns
        -------
        selected_frames : { a -> b }
            A map of frame number a to the frame data b
        '''
        selected_frames, _ = self.get_segment_frames_with_stats(
            video_file, save_stats_for_all_frames=False
        )
        return selected_frames

    def get_segment_frames_with_stats(self, video_file, save_stats_for_all_frames=True):
        ''' Returns a list of frames for the best possible video segments (refer to get_best_segment_frames())
        
        It also outputs statistics on all frames, where the statistic on frame i is:
        {
            "timestamp": the timestamp of frame i
            "num_pixels_changed": number of pixel changes from frame i - 1 to frame i
        }

        Returns
        -------
        selected_frames : { a -> b }
            A map of frame number to its frame data
        stats : { a -> c }
            A map of frame number to its statistic
        '''

        video_reader = cv2.VideoCapture(video_file)

        # Get the Default resolutions
        frame_width = int(video_reader.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(video_reader.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Get the FPS
        fps = int(video_reader.get(cv2.CAP_PROP_FPS))
        print(fps)

        frame_num = 0
        frame_num_to_stats = {}
        selected_frames = {}

        width = (video_reader.get(cv2.CAP_PROP_FRAME_WIDTH))   
        height  = (video_reader.get(cv2.CAP_PROP_FRAME_HEIGHT))   

        h = float(0.41243459526008003)
        w = float(0.6902123730378579)
        x = float(0.2812211445273895)
        y = float(0.14212065407394983)
        start_time = 345
        end_time = 712

        start_frame_num = cal_time_to_frame(start_time, fps)
        end_frame_num = cal_time_to_frame(end_time, fps)
        print(start_frame_num, end_frame_num)

        prev_timestamp = 0
        prev_frame = 255 * np.ones(
            (frame_height, frame_width, 3), np.uint8
        )  # A blank screen
        prev_frame = prev_frame[int(height*y): int(height*(y + h)), int(width*x): int(width*(x + w))]

        prev_video_changes = PastFrameChangesTracker()

        video_reader.set(cv2.CAP_PROP_POS_FRAMES, start_frame_num -1)
        frame_num = start_frame_num -1

        while video_reader.isOpened():

            is_read, cur_frame = video_reader.read()
            cur_frame = cur_frame[int(height*y): int(height*(y + h)), int(width*x): int(width*(x + w))]
            #cur_frame = np.array(cur_frame)
                        
            timestamp = video_reader.get(cv2.CAP_PROP_POS_MSEC)

            # Is when the stream is ending
            if not is_read:
                break

            if(frame_num>end_frame_num):
                break

            if(frame_num%(fps/2)==0 and frame_num>start_frame_num and frame_num<end_frame_num):
                #print(frame_num)
                results = self.__compare_frames__(prev_frame, cur_frame)

                # Store the results
                if save_stats_for_all_frames:
                    frame_num_to_stats[frame_num] = {
                        "timestamp": timestamp,
                        "num_pixels_changed": results["num_pixels_changed"],
                    }

                has_changed = results["num_pixels_changed"] > self.min_change
                has_changed2 = results["num_pixels_changed"] < self.max_change
                save_frame = False

                #if prev_video_changes.are_previous_frames_stable() and has_changed and has_changed2:
                if has_changed and has_changed2:
                    save_frame = True

                if save_frame:
                    selected_frames[frame_num] = {
                        "timestamp": prev_timestamp,
                        "frame": prev_frame,
                        "next_frame": cur_frame,
                        "mask": results["mask"],
                        "num_pixels_changed": results["num_pixels_changed"],
                    }

                prev_video_changes.add_frame_change(has_changed)

                prev_frame = cur_frame
                prev_timestamp = timestamp

            frame_num += 1

        # Add the last frame of the video
        selected_frames[frame_num] = {
            "timestamp": prev_timestamp,
            "frame": prev_frame,
            "next_frame": 255
            * np.ones((frame_height, frame_width, 3), np.uint8),  # A blank screen,
            "mask": prev_frame,
            "num_pixels_changed": 0,
        }

        # Rare case: if there are two selected frames s.t. they differ by 1 second, then there is a glitch
        # and we pick the frame that is the earliest
        selected_frame_nums = sorted(selected_frames.keys())
        i = 0
        while i < len(selected_frame_nums) - 1:
            cur_frame = selected_frames[selected_frame_nums[i]]
            next_frame = selected_frames[selected_frame_nums[i + 1]]

            if (next_frame["timestamp"] - cur_frame["timestamp"]) < 2000:
                del selected_frames[selected_frame_nums[i + 1]]
                i += 1

            i += 1

        # Edge case: delete the first selected frame since it is just a blank screen
        del selected_frames[selected_frame_nums[0]]

        video_reader.release()
        cv2.destroyAllWindows()

        return selected_frames, frame_num_to_stats

    def __compare_frames__(self, prev_frame, cur_frame):
        diff = cv2.absdiff(prev_frame, cur_frame)
        mask = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        num_pixels_changed = np.sum(mask > self.threshold)
        print("num_pixels_changed:"+str(num_pixels_changed))
        #print("num_pixels_changed:"+str(num_pixels_changed)+" mask:"+str(mask)+" diff:"+str(diff))

        return {"num_pixels_changed": num_pixels_changed, "mask": mask, "diff": diff}


if __name__ == "__main__":
    splitter = VideoSegmentFinder()
    splitter.get_best_segment_frames("../tests/videos/input_2.mp4")
