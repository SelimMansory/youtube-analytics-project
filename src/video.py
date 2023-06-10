import os
from googleapiclient.discovery import build
import json


class Video:

    api_key: str = os.environ.get('YT_API_KEY')
    # создать специальный объект для работы с API
    youtube = build('youtube', 'v3', developerKey = api_key)

    def __init__(self, id_video: str) -> None:
        self.id_video = id_video
        video = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                       id=self.id_video
                                       ).execute()
        self.name_video = video['items'][0]['snippet']['title']
        self.link_on_video = f'https://youtu.be/{self.name_video}'
        self.view_count = video['items'][0]['statistics']['viewCount']
        self.like_count = video['items'][0]['statistics']['likeCount']

    def __str__(self):
        return self.name_video

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.id_video}')"


class PLVideo(Video):

    api_key: str = os.environ.get('YT_API_KEY')
    # создать специальный объект для работы с API
    youtube = build('youtube', 'v3', developerKey = api_key)

    def __init__(self, id_video, id_playlist):
        super().__init__(id_video)
        self.id_playlist = id_playlist

    def __str__(self):
        return self.name_video

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.id_video}','{self.id_playlist}')"
