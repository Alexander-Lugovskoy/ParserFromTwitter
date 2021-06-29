import os

# BEARER был выявлен путем анализа запросов на сайте, вроде никогда не
# меняется.
BEARER = "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA"
# абсолютный путь до корневой папки проекта
base_path = os.path.dirname(os.path.abspath(__file__))
BASE_PATH = base_path + "\\"
LOGS_BASE_PATH = BASE_PATH + 'logs\\'  # местоположение лог-файлов
# местоположение логов твитов по дефолту
LOGS_TWEETS_DEFAULT_DIR = LOGS_BASE_PATH + 'tweets\\'
