"""
twitter_test.py
A standalone script to test your Twitter/X API integration automatically.
"""

import django
import os
import sys

# ----------------------------------------------------
# 1. Configure Django so we can access settings + code
# ----------------------------------------------------
# Adjust path if your manage.py lives somewhere else
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

sys.path.append(PROJECT_ROOT)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "news_app.settings")

django.setup()

# ----------------------------------------------------
# 2. Import your Tweet class
# ----------------------------------------------------
from newsapp.functions.twitter_api import Tweet


# ----------------------------------------------------
# 3. Test tweet function
# ----------------------------------------------------
def test_twitter_api():
    print("Initializing Twitter test…")

    tw = Tweet()

    message = "🌐 Twitter API Test — Sent from testing script"

    print("Sending test tweet...")
    result = tw.make_tweet(message)

    print("\n----- RESULT -----")
    print(result)
    print("------------------\n")


# ----------------------------------------------------
# 4. Run when executed as a script
# ----------------------------------------------------
if __name__ == "__main__":
    test_twitter_api()
