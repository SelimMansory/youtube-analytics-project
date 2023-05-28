import json
import os
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб - канала"""
    # YT_API_KEY скопирован из гугла и вставлен в переменные окружения
    api_key: str = os.environ.get('YT_API_KEY')

    # создать специальный объект для работы с API
    youtube = build('youtube', 'v3', developerKey = api_key)


    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала.
        Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id

        channel = self.youtube.channels().list \
            (id = channel_id, part = 'snippet,statistics').execute()

        self.title = channel['items'][0]['snippet']['title']
        self.description = channel['items'][0]['snippet']['description']
        self.url = 'https://www.youtube.com/channel/' + self.__channel_id
        self.subscriber_count = channel['items'][0]['statistics']['subscriberCount']
        self.video_count = channel['items'][0]['statistics']['videoCount']
        self.view_count = channel['items'][0]['statistics']['viewCount']


    @property

    def channel_id(self):
        return self.__channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = self.youtube.channels().list\
        (id = self.channel_id, part = 'snippet,statistics').execute()
        print(channel)


    def to_json(self, name: str) -> None:
        """
        Запись класса в файл
        """
        a = self.__dict__
        with open(name, 'w', encoding='utf-8') as f:
            json.dump(a, f)


    @classmethod
    def get_service(cls):
        return cls.youtube
