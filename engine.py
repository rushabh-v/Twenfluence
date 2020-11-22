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
    figure = plot.get_graph(top_influencers)
