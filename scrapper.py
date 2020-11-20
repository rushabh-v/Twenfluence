import tweepy
import json
from collections import defaultdict

from passwords import TWITTER_KEY, TWITTER_SECRET


auth = tweepy.OAuthHandler(TWITTER_KEY, TWITTER_SECRET)
api = tweepy.API(auth)

templates_file = open("./templates.json")
templates = json.load(templates_file)
wrapper = templates["wrapper_template"]
user_template = templates["user_template"]
tweet_template = templates["tweet_template"]

def get_users_and_tweets(hashtag):
    users = defaultdict(list)
    tweets = defaultdict()

    for tweet in tweepy.Cursor(api.search, q=hashtag, rpp=100).items(10 ** 10):
        # TO-DO (rushabh-v): Add location and lang filters
        if not hasattr(tweet, 'retweeted_status'):
            users[tweet.author.screen_name].append(tweet.id)
            tweet_details = tweet_template.copy()
            tweet_details["link"] = tweet.id
            tweet_details["n_likes"] = tweet.favorite_count
            tweet_details["n_retweets"] = tweet.retweet_count
            tweet_details["score"] = tweet.retweet_count + (0.4 * tweet.favorite_count)
            tweets[tweet.id] = tweet_details

    return users, tweets


# Updates the list in-place
def get_last_at_pos(arr):
    for i in range(len(arr)-1, 0, -1):
        if arr[i]["user_score"] > arr[i-1]["user_score"]:
            arr[i], arr[i-1] = arr[i-1], arr[i]


def get_top_influencers(hashtag, threshold, users, tweets):

    cur_min, most_influential = 0, []
    for username in users:
        total_retweets, total_likes, user_score = 0, 0, 0
        for id_ in users[username]:
            user_score += tweets[id_]["score"]
            total_likes += tweets[id_]["n_likes"]
            total_retweets += tweets[id_]["n_retweets"]

        if user_score > cur_min:
            USER = api.get_user(username)
            usr = user_template.copy()
            usr["username"] = username
            usr["name"] = USER.name
            usr["n_followers"] = USER.followers_count
            usr["n_tweets"] = len(users[username])
            usr["total_likes"] = total_likes
            usr["total_retweets"] = total_retweets
            usr["user_score"] = user_score
            usr["tweets"] = [tweets[id_] for id_ in users[username]]

            if len(most_influential) < threshold:
                most_influential.append(usr)
            else:
                most_influential[-1] = usr

            get_last_at_pos(most_influential)
            cur_min = most_influential[-1]["user_score"]

    wrapper["hashtag"] = hashtag
    wrapper["threshold"] = threshold
    wrapper["data"] = most_influential

    # Temporary (until the frontend is not done)
    prettyJson = json.dumps(wrapper, indent=4, separators=(',', ': '), sort_keys=True)
    print(prettyJson)

    return wrapper
