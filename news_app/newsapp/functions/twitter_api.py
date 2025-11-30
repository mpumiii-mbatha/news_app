"""Imported third-party API"""
from requests_oauthlib import OAuth1Session


class Tweet:
    """
    Class defining the Twitter API Key and Secret
    """
    CONSUMER_KEY = 'c3G10g97JtMivVbtudWZomjF7'
    CONSUMER_SECRET = 'a6KpLQED5GDh0Wl1BTir9BygpTwKHX8uvsh1rpJfitReDTk3SZ'

    _instance = None
    session = None

    def __new__(cls):
        if cls._instance is None:
            print("Creating the object")
            cls._instance = super(Tweet, cls).__new__(cls)
            cls._instance.oauth = cls._instance.authenticate()
        return cls._instance

    def authenticate_twitter(self):
        """"
        Third-party API (Twitter) authentication
        """

        request_token_url = (
            "https://api.twitter.com/oauth/request_token?"
            "oauth_callback=oob&x_auth_access_type=write"
            )

        oauth = OAuth1Session(self.CONSUMER_KEY,
                              client_secret=self.CONSUMER_SECRET)

        try:
            fetch_response = oauth.fetch_request_token(request_token_url)
        except ValueError:
            print("There is an issue with your consumer key or secret")

        resource_owner_key = fetch_response.get("oauth_token")
        resource_owner_secret = fetch_response.get("oauth_token_secret")
        print(f"Got OAuth token: {resource_owner_key}")

        # Request app authorisation from the user
        base_authorization_url = "https://api.twitter.com/oauth/authorize"
        authorization_url = oauth.authorization_url(base_authorization_url)
        print(f"Please go here and authorize: {authorization_url}")

        verifier = input("Paste the PIN here: ")

        access_token_url = "https://api.twitter.com/oauth/access_token"
        oauth = OAuth1Session(
            self.CONSUMER_KEY,
            client_secret=self.CONSUMER_SECRET,
            resource_owner_key=resource_owner_key,
            resource_owner_secret=resource_owner_secret,
            verifier=verifier
        )

        oauth_tokens = oauth.fetch_access_token(access_token_url)

        access_token = oauth_tokens["oauth_token"]
        access_token_secret = oauth_tokens["oauth_token_secret"]

        print(f"Access Token- {access_token}"
              f"Access Token Secret- {access_token_secret}")

        # Return session that has been authorised
        oauth = OAuth1Session(
            self.CONSUMER_KEY,
            client_secret=self.CONSUMER_SECRET,
            resource_owner_key=resource_owner_key,
            resource_owner_secret=access_token_secret,
        )

    def make_tweet(self, tweet):
        """
        Post a tweet
        """
        url = "https://api.twitter.com/1.1/statuses/update.json"
        response = self.session.post(url, data=tweet)
        if response.status_code == 200:
            print("Tweet posted")
        else:
            print(f"Try again: {response.text}")
