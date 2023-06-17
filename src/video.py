import os
from googleapiclient.discovery import build
import json
from src.channel import MixinYoutube


class Video(MixinYoutube):
    def __init__(self, id_video: str) -> None:
        try:
            self.id_video = id_video
            video = self.info_video(id_video)
            self.title = video['items'][0]['snippet']['title']
            self.link_on_video = f'https://youtu.be/{self.title}'
            self.view_count = video['items'][0]['statistics']['viewCount']
            self.like_count = video['items'][0]['statistics']['likeCount']
        except IndexError:
            print('Неверный id видео')
            self.title, self.like_count, self.link_on_video, self.view_count = None, None, None, None


    def __str__(self):
        return self.title

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.id_video}')"


class PLVideo(Video):

    def __init__(self, id_video, id_playlist):
        super().__init__(id_video)
        self.id_playlist = id_playlist

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.id_video}','{self.id_playlist}')"
