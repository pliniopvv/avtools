from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Thumbnail:
    url: str
    width: Optional[int] = None
    height: Optional[int] = None

@dataclass
class Format:
    format_id: str
    ext: str
    resolution: Optional[str] = None
    url: str = ""
    filesize: Optional[int] = None
    vcodec: Optional[str] = None
    acodec: Optional[str] = None

@dataclass
class VideoInfo:
    id: str
    title: str
    uploader: Optional[str] = None
    channel_id: Optional[str] = None
    upload_date: Optional[str] = None
    duration: Optional[int] = None
    view_count: Optional[int] = None
    like_count: Optional[int] = None
    dislike_count: Optional[int] = None
    description: Optional[str] = None
    categories: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    thumbnails: Optional[List[Thumbnail]] = None
    formats: Optional[List[Format]] = None
