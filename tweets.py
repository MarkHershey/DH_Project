# https://github.com/taspinar/twitterscraper
from markkk.logger import logger
from twitterscraper import query_tweets


query_tweets('query', limit=None, begindate=dt.date.today(), enddate=dt.date.today(), poolsize=20, lang='')