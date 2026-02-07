from moviepy.editor import VideoFileClip, concatenate_videoclips, cvsecs, vfx, clips_array

class MontConcatStrategy():

    def __init__(self, video_paths: list[str] = []):
        self.video_paths = video_paths
    
    def save(self, output_path: str):
        clips = [VideoFileClip(video) for video in self.video_paths]
        final_clip = concatenate_videoclips(clips)
        final_clip.write_videofile(output_path)
        for clip in clips:
            clip.close()
        final_clip.close()

    def close(self):
        ...

class MontMidnightStrategy():

    def __init__(self, video_paths: list[str] = []):
        self.video_paths = video_paths


    def save(self, output_path: str = "join_video.mp4"):
        # for video in self.repo:
        #     width = video.size[0]
        #     height = video.size[1]
        #     if width > mWidth:
        #         mWidth = width
        #     if height > mHeight:
        #         mHeight = height

        # totaltime = 0
        # for video in self.repo:
        #     totaltime += video.duration

        # video_resized = []
        # for video in self.repo:
        #     video_resized.append(video.resize((width, height)))
        # pass
        cont = -1
        videos = []
        for video in self.video_paths:
            cont += 1
            
            itfreeze = cvsecs(0.1)
            ftfreeze = cvsecs(video.duration-0.1)
            i_im_freeze = video.to_ImageClip(itfreeze).fx(vfx.blackwhite)
            f_im_freeze = video.to_ImageClip(ftfreeze)

            before = True
            fconcat = []
            for _video in self.video_paths:
                if video == _video:
                    fconcat.append(video)
                elif before:
                    fconcat.append(i_im_freeze.set_duration(_video.duration))
                else:
                    fconcat.append(f_im_freeze.set_duration(_video.duration))
            concat = concatenate_videoclips(fconcat)
            videos.append([concat])

        result = clips_array(videos)
        result.write_videofile(output_path)
    

    