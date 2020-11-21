import sys
import scrapper
import plot

import seaborn as sns
from collections import defaultdict
import pandas as pd
import numpy as np

if __name__ == '__main__':
    # Will be received from the frontend
    hashtag = sys.argv[1]
    threshold = 10
    location = ""
    language = ""

    users, tweets = scrapper.get_users_and_tweets(hashtag)
    top_influencers, top_tweets = scrapper.get_top_influencers(hashtag, threshold, users, tweets)

    tweet_scores = defaultdict(list)
    max_len = 0
    for user in top_influencers["data"]:
        for tweet in user["tweets"]:
            tweet_scores[user["username"]].append(tweet["score"])
            max_len = max(max_len, len(tweet_scores[user["username"]]))

    for user in tweet_scores:
        scores = tweet_scores[user]
        if len(scores) < max_len:
            mean = np.mean(scores)
            scores.extend([mean] * (max_len-len(scores)))
            tweet_scores[user] = scores

    figure = plot.plot_data(tweet_scores)
