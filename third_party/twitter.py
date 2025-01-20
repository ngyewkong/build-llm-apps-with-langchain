import os
from dotenv import load_dotenv
import tweepy
import requests

load_dotenv()

twitter_client = tweepy.Client(
    bearer_token=os.environ["TWITTER_BEARER_TOKEN"],
    consumer_key=os.environ["TWITTER_API_KEY"],
    consumer_secret=os.environ["TWITTER_API_KEY_SECRET"],
    access_token=os.environ["TWITTER_ACCESS_TOKEN"],
    access_token_secret=os.environ["TWITTER_ACCESS_TOKEN_SECRET"],
)


def scrape_user_tweets(username, num_tweets=5, mock: bool = False):
    """
    Scrapes a Twitter user's original tweets (i.e., not retweets or replies) and returns them as a list of dictionaries.
    Each dictionary has three fields: "time_posted" (relative to now), "text", and "url".
    """
    tweet_list = []
    if mock:
        # use pre downloaded tweets (need to use the raw version of gist if not will have html being returned)
        TWITTER_GIST = "https://gist.githubusercontent.com/ngyewkong/db915a5f16ea1ad2db99962ab8680e15/raw/7f36061a4b794b5994188706b8813508ab27d68a/sample_mock_tweets.json"
        response = requests.get(TWITTER_GIST, timeout=5)
        print(response)
        response.raise_for_status()
        if response.status_code != 204:
            tweets = response.json()
    # if not mocking -> use twitter api but not free
    else:
        user_id = twitter_client.get_user(username=username,).data.id
        tweets = twitter_client.get_users_tweets(
            id=user_id,
            max_results=num_tweets,
            exclude=["retweets", "replies"]
        )
        tweets = tweets.data

    for tweet in tweets:
        tweet_dict = {}
        tweet_dict["text"] = tweet["text"]
        tweet_dict["url"] = f"https://twitter.com/{username}/status/{tweet['id']}"
        tweet_list.append(tweet_dict)

    return tweet_list


if __name__ == "__main__":
    tweets = scrape_user_tweets(username="ngyewkong", mock=True)
    print(tweets)
