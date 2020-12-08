from twitter_scraper import get_tweets

for tweet in get_tweets('BarackObama', pages=1):
    print(tweet['text'])