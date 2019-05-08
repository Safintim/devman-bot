import os
import requests
import telegram
from dotenv import load_dotenv


class SecretData:
    def __init__(self):
        self.token_devman = os.getenv('TOKEN_DEVMAN')
        self.token_bot = os.getenv('TOKEN_TELEGRAM')
        self.chat_id = os.getenv('CHAT_ID')


class Message:
    def __init__(self, header=None, neg_true=None, neg_false=None, bottom=None):
        self.header = header or 'У вас проверили работу "{}"\n\nСсылка на задачу: https://dvmn.org{}\n\n'
        self.is_negative_true = neg_true or 'О, да! Красава! Пора приступать к следующей!'
        self.is_negative_false = neg_false or 'Есть ошибки, пора работать..'
        self.bottom = bottom or ''


class BotDevman:
    def __init__(self, secret_data, message=None):
        self.bot = telegram.Bot(secret_data.token_bot)
        self.secret_data = secret_data
        self.message = Message() or message

    def compose_message(self, tasks):
        for task in tasks:
            msg = self.message.header.format(task['lesson_title'], task['lesson_url'])
            if task['is_negative']:
                msg += self.message.is_negative_true
            else:
                msg += self.message.is_negative_false
            msg += self.message.bottom
            return msg

    def request_to_devman(self, params):
        api_url = 'https://dvmn.org/api/long_polling/'
        headers_devman = {
            'Authorization': 'Token {}'.format(self.secret_data.token_devman)
        }

        response = requests.get(api_url, headers=headers_devman, params=params)
        response.raise_for_status()
        response_json = response.json()

        if 'timestamp_to_request' in response_json:
            return response_json['timestamp_to_request'], None
        elif 'last_attempt_timestamp' in response_json:
            return response_json['last_attempt_timestamp'], response_json

    def listen_devman(self):
        params = {}
        while True:
            try:
                timestamp, response = self.request_to_devman(params)
                if response:
                    self.bot.send_message(chat_id=self.secret_data.chat_id,
                                          text=self.compose_message(response['new_attempts']))
                params['timestamp'] = timestamp
            except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError,
                    requests.exceptions.HTTPError) as e:
                print(e)


def main():
    load_dotenv()
    secret_data = SecretData()
    BotDevman(secret_data).listen_devman()


if __name__ == '__main__':
    main()
