from collections import defaultdict

import numpy as np
import pandas as pd
import seaborn as sns


def get_plot(data):
    df = pd.DataFrame.from_dict(data)
    sns.set_style('ticks')
    plt = sns.boxplot(data=df)
    plt.set_xticklabels(labels=plt.get_xticklabels(), rotation=45)
    sns.despine()
    figure = plt.get_figure()
    return figure


def get_graph(top_influencers):

    max_len, tweet_scores = 0, defaultdict(list)
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

    figure = get_plot(tweet_scores)
    figure.savefig("./img/output.png", bbox_inches = "tight")
    # figure.savefig("./output.png", bbox_inches = "tight")
    return figure
