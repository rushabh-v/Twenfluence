import sys
import scrapper

if __name__ == '__main__':
    # Will be received from the frontend
    hashtag = sys.argv[1]
    threshold = 10
    location = ""
    language = ""

    users, tweets = scrapper.get_users_and_tweets(hashtag)
    top_influencers = scrapper.get_top_influencers(hashtag, threshold, users, tweets)
