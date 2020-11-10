import re
from typing import List


class Tweet:
    def __init__(self, id: str, text: str, user_name: str, data: dict):
        self.id = id
        self.text = text
        self.hashtags = self.find_hashtags()
        self.user_name = user_name
        self.raw_data = data
        if self.is_retweet():
            self.set_retweet_text()

    def get_url(self) -> str:
        return 'https://twitter.com/{}/status/{}'.format(
            self.user_name,
            self.id
        )

    def is_retweet(self):
        # The is_retweet flag in the api response is not working
        return 'RT @' in self.text

    def set_retweet_text(self):
        if self.raw_data.get('retweeted_status'):
            self.text = self.raw_data.get('retweeted_status')['full_text']

    def find_hashtags(self) -> List[str]:
        return re.findall(r"#(\w+)", self.text)

    def to_dict(self) -> dict:
        return {
            'text': self.text,
            'hashtags': self.hashtags,
            'link': self.get_url(),
            'user': self.user_name
        }
