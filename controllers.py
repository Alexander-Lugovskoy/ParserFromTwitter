import twitter_api
import helpers


def parseTweets(username: str, count: int):
    """
    Получим твиты конкретного юзера и запишим их в лог
    :param username: никнейм из твиттера, чьи твиты нужно получить
    :param count: количество твитов
    """
    tweets = twitter_api.UserTweets(username, count)
    clear_tweets = helpers.getTweetsOnly(tweets)
    helpers.logTwitts(username, clear_tweets)
