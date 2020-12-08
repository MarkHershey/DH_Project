# https://github.com/taspinar/twitterscraper
from markkk.logger import logger
from twitterscraper import query_tweets


# query_tweets('query', limit=None, begindate=dt.date.today(), enddate=dt.date.today(), poolsize=20, lang='')

if __name__ == "__main__":
    list_of_tweets = query_tweets("Ivanka Trump", 10)

    # print the retrieved tweets to the screen:
    for tweet in query_tweets("Ivanka Trump", 10):
        print(tweet)

    # Or save the retrieved tweets to file:
    file = open("output.txt", "w")
    for tweet in query_tweets("Ivanka Trumpn", 10):
        file.write(str(tweet.text.encode("utf-8")))
    file.close()
