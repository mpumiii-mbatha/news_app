"""Twitter API Tweepy (V2 OAuth 2.0 User Context)"""
from django.conf import settings
import tweepy


class Tweet:
    """
    Modern Tweet class using Tweepy Client (Twitter API v2)
    Works with OAuth 2.0 User Context.
    """

    def __init__(self):
        self.client = tweepy.Client(
            bearer_token=settings.TWITTER_BEARER_TOKEN,
            consumer_key=settings.TWITTER_CONSUMER_KEY,
            consumer_secret=settings.TWITTER_CONSUMER_SECRET,
            access_token=settings.TWITTER_ACCESS_TOKEN,
            access_token_secret=settings.TWITTER_ACCESS_TOKEN_SECRET
        )

    def make_tweet(self, text: str):
        """
        Post a tweet using Twitter API v2 create_tweet.
        Automatically handles rate-limit or permission errors.
        """
        try:
            response = self.client.create_tweet(text=text)

            # Successful response
            if response.data and "id" in response.data:
                print(f"Tweet posted successfully: {response.data['id']}")
                return response.data

        except tweepy.Forbidden as e:
            # Happens on free-tier access restrictions
            print(f"[Tweet blocked by API restrictions]: {text}")
            print(str(e))

        except tweepy.TweepyException as e:
            print(f"Error posting tweet: {str(e)}")

        return None
