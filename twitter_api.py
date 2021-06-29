import requests
from requests.exceptions import HTTPError
import config
import logging

logging.basicConfig(filename='api_debug.log', level=logging.DEBUG)


def _getCookies() -> dict:
    """
    просто шлем запрос на видео случайного твита,
    чтобы получить хранящиеся в куках
    personalization_id и guest_id,
    необходимые для получения guest_token
    """
    try:
        r = requests.get(
            "https://twitter.com/i/videos/tweet/1407075914140176390")
        r.raise_for_status()
    except HTTPError as http_err:
        logging.warning(f'HTTP error occurred: {http_err}')
        exit(1)
    except Exception as err:
        logging.warning(f'Other error occurred: {err}')
        exit(1)
    else:
        set_cookie = r.headers.get("set-cookie")
        logging.debug(f'headers: {r.headers}')
        logging.debug(f'set-cookie: {set_cookie}')
        return set_cookie


def _getGuestToken() -> str:
    """
    Получает guest_token, необходимый для доступа к API.
    guest_token периодически становится не ликвидным,
    я не стал досканально разбираться как часто его нужно получать,
    но вроде живет он не менее 2-ух часов,
    я его для каждого запроса получаю заного сейчас
    """
    try:
        r = requests.post(
            "https://api.twitter.com/1.1/guest/activate.json",
            headers={
                'Accept-Encoding': 'gzip, deflate, br, utf-8',
                'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
                'authorization': config.BEARER,
                'cookie': _getCookies()})
        r.raise_for_status()
    except HTTPError as http_err:
        logging.warning(f'HTTP error occurred: {http_err}')
        exit(1)
    except Exception as err:
        logging.warning(f'Other error occurred: {err}')
        exit(1)
    else:
        guest_token = r.json().get("guest_token")
        logging.debug(f"guest_token: {guest_token}")
        return guest_token


def _UserByScreenName(screen_name: str) -> int:
    """
    Получаем информацию о пользователе по его никнейму
    в первую очередь нас интересует rest_id, находящийся там.
    По rest_id мы можем получать твиты пользователя
    Функцию можно быстро модифицировать, чтобы она возвращала обширный набор информации о юзере,
    сейчас возвращает rest_id юзера (int)
    """
    prepare_variables = '{"screen_name":"%s","withHighlightedLabel":true}' % screen_name
    try:
        r = requests.get(
            'https://twitter.com/i/api/graphql/4ti9aL9m_1Rb-QVTuO5QYw/UserByScreenNameWithoutResults',
            params={
                'variables': prepare_variables},
            headers={
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, br, utf-8',
                'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
                'authorization': config.BEARER,
                'x-guest-token': _getGuestToken(),
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'content-type': 'application/json',
                'DNT': '1',
                'Host': 'twitter.com',
                'Pragma': 'no-cache',
                'Referer': 'https://twitter.com',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0',
            })
        r.raise_for_status()
    except HTTPError as http_err:
        logging.warning(f'HTTP error occurred: {http_err}')
        exit(1)
    except Exception as err:
        logging.warning(f'Other error occurred: {err}')
        exit(1)
    else:
        rest_id = r.json().get('data').get('user').get('rest_id')
        logging.debug(f'Success! rest_id: {rest_id}')
        return rest_id


def UserTweets(screen_name: str, count: int):
    """
    получаем указанное количество твитов указанного пользователя
    screen_name - отображаемое имя пользователя твиттера
    count - количество твитов, которое хотите получить
    """
    screen_name = screen_name.lower()
    userId = str(_UserByScreenName(screen_name))
    try:
        r = requests.get(
            'https://twitter.com/i/api/graphql/TcBvfe73eyQZSx3GW32RHQ/UserTweets',
            params={
                'variables': '{"userId":"%s","count":%d,"withHighlightedLabel":true,"withTweetQuoteCount":true,"includePromotedContent":true,"withTweetResult":true,"withReactions":false,"withSuperFollowsTweetFields":false,"withUserResults":false,"withVoice":false,"withNonLegacyCard":true,"withBirdwatchPivots":false}' % (userId,
                                                                                                                                                                                                                                                                                                                                  count)},
            headers={
                'Accept': '*/*',
                'Accept-Encoding': 'utf-8',
                'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
                'authorization': config.BEARER,
                'x-guest-token': _getGuestToken(),
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'content-type': 'application/json',
                'DNT': '1',
                'Host': 'twitter.com',
                'Pragma': 'no-cache',
                'Referer': 'https://twitter.com',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0',
            })
        r.raise_for_status()
    except HTTPError as http_err:
        logging.warning(f'HTTP error occurred: {http_err}')
        exit(1)
    except Exception as err:
        logging.warning(f'Other error occurred: {err}')
        exit(1)
    else:
        return (r.json())
