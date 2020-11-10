import os
from requests import Response, get
from collections import Counter
from typing import List

from .classes import Tweet


class TwitterService:
    url: str = 'https://api.twitter.com/1.1/search/tweets.json'

    @classmethod
    def get_100_tweets(cls, term: str, language: str):
        response = cls.get_twitter_top_100({
            'q': term,
            'count': 100,
            'lang': language,
            'tweet_mode': 'extended'
        })
        if response.ok:
            data = response.json()
            tweets = []
            hashtags = []
            for status in data['statuses']:
                tweet = Tweet(
                    status['id'],
                    status['full_text'],
                    status['user']['screen_name'],
                    status
                )
                tweets.append(tweet.to_dict())
                hashtags.extend(tweet.hashtags)
            return {
                'tweets': tweets,
                'hashtags': cls.count_hashtags(hashtags)
            }
        raise ValueError(
            'The following error happened: ' + str(response.json())
        )

    @classmethod
    def get_twitter_top_100(cls, params: dict) -> Response:
        return get(
            cls.url,
            params=params,
            headers={
                'Authorization': 'Bearer {}'.format(
                    os.environ['TWITTER_BEARER_TOKEN']
                )
            }
        )

    @staticmethod
    def count_hashtags(hashtags: List[str]):
        return [{
            'count': count,
            'hashtag': hashtag
        } for hashtag, count in Counter(hashtags).most_common(10)]
