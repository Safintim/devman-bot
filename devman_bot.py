import os
import requests
import telegram
from dotenv import load_dotenv
from pprint import pprint


def compose_message(response):
    message = 'У вас проверили работу "{}"\n\nСсылка на задачу: https://dvmn.org{}\n\n'
    for task in response['new_attempts']:
        message = message.format(task['lesson_title'], task['lesson_url'])
        if task['is_negative']:
            message += 'О, да! Красава! Пора приступать к следующей!'
        else:
            message += 'Есть ошибки, пора работать..'

    return message


def get_secret_data():
    return os.getenv('TOKEN_DEVMAN'), os.getenv('TOKEN_TELEGRAM'), os.getenv('CHAT_ID')


def listen_devman(api_url, token_devman, params):
    headers_devman = {
        'Authorization': 'Token {}'.format(token_devman)
    }
    response = requests.get(api_url, headers=headers_devman, params=params)
    if 'timestamp_to_request' in response.json():
        return response.json()['timestamp_to_request'], None
    elif 'last_attempt_timestamp' in response.json():
        return response.json()['last_attempt_timestamp'], response.json()


def main():
    load_dotenv()
    token_devman, token_bot, chat_id = get_secret_data()
    api_url = 'https://dvmn.org/api/long_polling/'
    bot = telegram.Bot(token=token_bot)

    params = {}
    while True:
        try:
            timestamp, response = listen_devman(api_url, token_devman, params)
            if response:
                bot.send_message(chat_id=chat_id, text=compose_message(response))
            params['timestamp'] = timestamp
        except requests.exceptions.ReadTimeout as e:
            print(e)


if __name__ == '__main__':
    main()
