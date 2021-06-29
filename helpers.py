from datetime import datetime
import config


def getTweetsOnly(TweetsByUser: dict) -> list:
    """
    переберает json из UserTweets, на выходе формирует двумерный массив
    с временной меткой поста и датой поста
    прмер выходных данных:
     [
         ['Sun Jun 27 14:11:23 +0000 2021'], ['текст твита'],
         ['Sun Jun 28 15:11:23 +0000 2021'], ['текст еще одного твита']
     ]
    """
    entries = TweetsByUser.get('data').get('user').get('result').get(
        'timeline').get('timeline').get('instructions')[0].get('entries')
    tweets = []
    if (entries is not None):
        for i in entries:
            itemContent = i.get('content').get('itemContent')
            if (itemContent is not None):
                result_legacy = itemContent.get(
                    'tweet_results').get('result').get('legacy')
                created_at = result_legacy.get('created_at')
                full_text = result_legacy.get('full_text')

                # проверяем есть текст в твите или нет
                # если есть, то добавляем в пулл
                if (full_text.find('https://t.co/') == -1):
                    tweet = [created_at, full_text]
                    tweets.append(tweet)

        return (tweets)
    else:
        tweets = [str(datetime.today()), "Твиты не найдены"]
        return (tweets)


def logTwitts(
        username: str,
        tweets: list,
        tweets_dir=config.LOGS_TWEETS_DEFAULT_DIR):
    f = open(tweets_dir + username + '.log', 'w', encoding="utf-8")
    for i in tweets:
        f.write(f"[{i[0]}] | {i[1]}\n")
    f.close()
