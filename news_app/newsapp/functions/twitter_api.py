"""Imported Modules"""
import json
import os
from django.conf import settings
from requests_oauthlib import OAuth1Session


class Tweet:
    """
    Tweet class
    """

    CONSUMER_KEY = settings.TWITTER_CONSUMER_KEY
    CONSUMER_SECRET = settings.TWITTER_CONSUMER_SECRET
    ACCESS_TOKEN = settings.TWITTER_ACCESS_TOKEN
    ACCESS_TOKEN_SECRET = settings.TWITTER_ACCESS_TOKEN_SECRET

    TOKEN_FILE = os.path.join(settings.BASE_DIR, "twitter_tokens.json")

    _instance = None
    session = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Tweet, cls).__new__(cls)
            cls._instance.authenticate_twitter()
        return cls._instance

    def authenticate_twitter(self):
        """
        Authenticate with Twitter API.
        Reuses saved access tokens if available.
        """

        # If you already have permanent access tokens, skip OAuth flow
        if self.ACCESS_TOKEN and self.ACCESS_TOKEN_SECRET:
            self.session = OAuth1Session(
                self.CONSUMER_KEY,
                client_secret=self.CONSUMER_SECRET,
                resource_owner_key=self.ACCESS_TOKEN,
                resource_owner_secret=self.ACCESS_TOKEN_SECRET
            )
            print("Authenticated using access token + secret from .env")
            return

        # Otherwise fall back to OAuth PIN-based flow
        if os.path.exists(self.TOKEN_FILE):
            with open(self.TOKEN_FILE, "r") as f:
                tokens = json.load(f)
            self.session = OAuth1Session(
                self.CONSUMER_KEY,
                client_secret=self.CONSUMER_SECRET,
                resource_owner_key=tokens["access_token"],
                resource_owner_secret=tokens["access_token_secret"]
            )
            print("Using saved Twitter tokens.")
            return

        try:
            self.session = OAuth1Session(
                self.CONSUMER_KEY,
                client_secret=self.CONSUMER_SECRET,
                resource_owner_key=self.ACCESS_TOKEN,
                resource_owner_secret=self.ACCESS_TOKEN_SECRET
            )
            # Simple test to confirm authentication
            url = "https://api.twitter.com/1.1/account/verify_credentials.json"
            response = self.session.get(url)
            if response.status_code == 200:
                print("Authenticated with Twitter API (read-only).")
            else:
                print(f"Authenticated, but got warning: {response.text}")
        except Exception as e:
            print(f"Error during Twitter auth: {e}")

        print("No tokens available. OAuth flow required (PIN).")

    def make_tweet(self, tweet_text):
        """
        Post a tweet.
        """
        if not self.session:
            print("f[Simulated tweet]: {tweet_text}")
            return

        url = "https://api.twitter.com/1.1/statuses/update.json"

        try:
            response = self.session.post(url, data={"status": tweet_text})
            if response.status_code == 200:
                print("Tweet posted successfully")
            elif response.status_code == 453:
                # Free-tier account restriction
                print(f"[Simulated tweet due to API limit]: {tweet_text}")
            else:
                print(f"Failed to post tweet: {response.text}")
        except Exception as e:
            print(f"[Tweet failed with exception]: {e}")
