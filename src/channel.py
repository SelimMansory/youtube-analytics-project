import json
import os

from googleapiclient.discovery import build


class MixinYoutube:
    # YT_API_KEY скопирован из гугла и вставлен в переменные окружения
    api_key: str = os.environ.get('YT_API_KEY')
    # создать специальный объект для работы с API
    youtube = build('youtube', 'v3', developerKey=api_key)

    def info_channel(self, channel):
        return self.youtube.channels().list(id=channel, part='snippet,statistics').execute()

    def info_video(self, id_video):
        return self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                          id=id_video
                                          ).execute()


class Channel(MixinYoutube):
    """Класс для ютуб - канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала.
        Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        try:
            self.__parse()
        except Exception as e:
            print("Error", str(e))

    def __parse(self):
        channel = self.youtube.channels().list \
            (id=self.__channel_id, part='snippet,statistics').execute()

        self.title = channel['items'][0]['snippet']['title']
        self.description = channel['items'][0]['snippet']['description']
        self.url = 'https://www.youtube.com/channel/' + self.__channel_id
        self.subscriber_count = channel['items'][0]['statistics']['subscriberCount']
        self.video_count = channel['items'][0]['statistics']['videoCount']
        self.view_count = channel['items'][0]['statistics']['viewCount']

    def __str__(self):
        return f'{self.title} ({self.url})'

    def __add__(self, other) -> int:
        return int(self.subscriber_count) + int(other.subscriber_count)

    def __sub__(self, other) -> int:
        return int(self.subscriber_count) - int(other.subscriber_count)

    def __gt__(self, other) -> bool:
        return int(self.subscriber_count) > int(other.subscriber_count)

    def __ge__(self, other) -> bool:
        return int(self.subscriber_count) >= int(other.subscriber_count)

    def __lt__(self, other) -> bool:
        return int(self.subscriber_count) < int(other.subscriber_count)

    def __le__(self, other) -> bool:
        return int(self.subscriber_count) <= int(other.subscriber_count)

    @property
    def channel_id(self):
        return self.__channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = self.youtube.channels().list\
            (id=self.channel_id, part='snippet,statistics').execute()
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


client = Channel("UCwHL6WHUarjGfUM_586me8w")
client.print_info()
