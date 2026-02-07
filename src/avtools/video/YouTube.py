from importlib.resources import path

from .Model import Format, Thumbnail
from . import VideoInfo
from yt_dlp import YoutubeDL
import logging

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class YoutubeVideo(VideoInfo):

    def __init__(self, href):
        logger.debug(f"Initializing Video with href: {href}")
        self.href = href
        with YoutubeDL() as ydl:
            json = ydl.extract_info(href, download=False)
            super().__init__(
                id=json.get('id', ''),
                title=json.get('title', ''),
                uploader=json.get('uploader'),
                channel_id=json.get('channel_id'),
                upload_date=json.get('upload_date'),
                duration=json.get('duration'),
                view_count=json.get('view_count'),
                like_count=json.get('like_count'),
                dislike_count=json.get('dislike_count'),
                description=json.get('description'),
                categories=json.get('categories'),
                tags=json.get('tags'),
                thumbnails=[
                    Thumbnail(
                        url=thumb['url'],
                        width=thumb.get('width'),
                        height=thumb.get('height')
                    ) for thumb in json.get('thumbnails', [])
                ] if json.get('thumbnails') else None,
                formats=[
                    Format(
                        format_id=fmt['format_id'],
                        ext=fmt['ext'],
                        resolution=fmt.get('resolution'),
                        url=fmt.get('url', ''),
                        filesize=fmt.get('filesize'),
                        vcodec=fmt.get('vcodec'),
                        acodec=fmt.get('acodec')
                    ) for fmt in json.get('formats', [])
                ] if json.get('formats') else None
            )
            logger.info(f"Video initialized: {self.title} (ID: {self.id})")
        ...

    def save(self, path=None):
        logger.debug(f"Saving video from {self.href} to {path}")
        if path is None:
            video_id = self.href.split("v=")[1].split("&")[0] if "v=" in self.href else "id_not_localized.mp4" #https://www.youtube.com/watch?v=90VfjbQytJc
            path = f"{video_id}.mp4"
        self.path = path
        ydl_opts = {
            'outtmpl': path,
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4',
        }
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.href])
        ...
        logger.info(f"Video saved to {path}")

    def getPath(self):
        logger.debug(f"Getting path for video: {self.href}")
        return self.path