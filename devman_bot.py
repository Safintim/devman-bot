import os
import logging
import requests
import telegram
from dotenv import load_dotenv


class SecretData:
    def __init__(self):
        self.token_devman = os.environ['TOKEN_DEVMAN']
        self.token_devman_bot = os.environ['TOKEN_DEVMAN_BOT']
        self.token_logger_bot = os.environ['TOKEN_LOGGER_BOT']
        self.chat_id = os.environ['CHAT_ID']


class Message:
    def __init__(self, header=None, positive=None, negative=None, bottom=None):
        self.header = header or 'У вас проверили работу "{}"\n\nСсылка на задачу: https://dvmn.org{}\n\n'
        self.is_positive = positive or 'О, да! Красава! Пора приступать к следующей!'
        self.is_negative = negative or 'Есть ошибки, пора работать..'
        self.bottom = bottom or ''


class LogsHandler(logging.Handler):

    def __init__(self,):
        super().__init__()
        self.bot = BotLogger()

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_report(log_entry)


class BotLogger:
    def __init__(self, secret_data=None):
        self.secret_data = secret_data or SecretData()
        self.bot = telegram.Bot(self.secret_data.token_logger_bot)

    @staticmethod
    def create_logger(logs_handler):
        logger = logging.getLogger('Bot Logger')
        handler = logs_handler()
        handler.setFormatter(logging.Formatter('%(message)s'))
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        return logger

    def send_report(self, msg):
        self.bot.send_message(chat_id=self.secret_data.chat_id, text=msg)


class BotDevman:
    def __init__(self, logger=None, secret_data=None, message=None):
        self.secret_data = secret_data or SecretData()
        self.message = message or Message()
        self.logger = logger
        self.bot = telegram.Bot(self.secret_data.token_devman_bot)

    def compose_message(self, tasks):
        for task in tasks:
            msg = self.message.header.format(task['lesson_title'], task['lesson_url'])
            if task['is_negative']:
                msg += self.message.is_positive
            else:
                msg += self.message.is_negative
            msg += self.message.bottom
            return msg

    def request_to_devman(self, params):
        api_url = 'https://dvmn.org/api/long_polling/'
        headers_devman = {
            'Authorization': 'Token {}'.format(self.secret_data.token_devman)
        }

        response = requests.get(api_url, headers=headers_devman, params=params)
        response.raise_for_status()
        data = response.json()

        if 'timestamp_to_request' in data:
            return data['timestamp_to_request'], None
        elif 'last_attempt_timestamp' in data:
            return data['last_attempt_timestamp'], data

    def listen_devman(self):
        params = {}
        while True:
            try:
                timestamp, response = self.request_to_devman(params)
                if response:
                    self.bot.send_message(chat_id=self.secret_data.chat_id,
                                          text=self.compose_message(response['new_attempts']))
                params['timestamp'] = timestamp
            except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError):
                continue
            except requests.exceptions.HTTPError:
                break

    def run(self):
        while True:
            try:
                self.logger.info('Бот запущен')
                self.listen_devman()
            except Exception as e:
                self.logger.warning('Бот упал')
                self.logger.error(e, exc_info=True)


def main():
    # load_dotenv()
    logger = BotLogger.create_logger(LogsHandler)
    BotDevman(logger=logger).run()


if __name__ == '__main__':
    main()
