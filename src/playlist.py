import os
from googleapiclient.discovery import build
import isodate
from datetime import timedelta
from src.channel import MixinYoutube


class PlayList(MixinYoutube):

    def __init__(self, id_playlist):
        self.id_playlist = id_playlist
        self.url = 'https://www.youtube.com/playlist?list=' + self.id_playlist
        self.title = self.youtube.playlists().list(part='snippet',
                                                   id=self.id_playlist
                                                   ).execute()['items'][0]['snippet']['localized']['title']
        # получение данные по видеороликам в плейлисте
        self.playlist_videos = self.youtube.playlistItems().list(playlistId=self.id_playlist,
                                                part='contentDetails',
                                                maxResults=50,
                                                ).execute()
        # получение списка ID видео
        self.video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        self.video_response = self.youtube.videos().list(part='contentDetails',
                                               id=','.join(self.video_ids)
                                               ).execute()
    @property
    def total_duration(self):
        # переменная для подсчета общего времени
        total_time = timedelta()
        for video in self.video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            time = str(duration).split(':')
            duration = timedelta(hours=int(time[0]), minutes=int(time[1]), seconds=int(time[2]))
            total_time += duration
        return total_time

    def show_best_video(self):
        statistics = self.youtube.videos().list(part='statistics, snippet',
                                               id=','.join(self.video_ids)
                                               ).execute()
        # количество лайков
        likes = [statistic['statistics']['likeCount'] for statistic in statistics['items']]
        return f'https://youtu.be/' + statistics['items'][likes.index(max(likes))]['id']