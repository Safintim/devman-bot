# devman-bot

## Описание
Бот для обучающихся на [девмане](https://dvmn.org/modules/). Высылает уведомление в телеграм,
если преподаватель проверил работу.


Использованные API: *[devman](https://dvmn.org/api/docs/)*

## Требования

Для запуска скрипта требуется:

*Python 3.6*


## Как установить:

1. Установить Python3:

(Windows):[python.org/downloads](https://www.python.org/downloads/windows/)

(Debian):
```sh
sudo apt-get install python3
sudo apt-get install python3-pip
```
2. Установить зависимости и скачать сам проект:

```sh
https://github.com/Safintim/devman-bot.git
pip3 install -r requirements.txt
```
3. Персональные настройки:

Скрипт берет настройки из файла .env, который содержит токен девмана, токен чат-девман-бота, токен чат-логгер-бота и номер чата в таком виде:
```sh
TOKEN_DEVMAN=your_token
TOKEN_DEVMAN_BOT=your_token
TOKEN_LOGGER_BOT=your_token
CHAT_ID=your_chat_id
```

## Зависимости
* *python-dotenv==0.10.1*
* *requests==2.21.0*
* *python-telegram-bot==11.1.0*

## Как использовать: 
Запустить скрипт:
```sh
python3 devman_bot.py
```

Найти ботов в телеграме **_@devvm_bot_**, **_@devmanlogging_bot_**

## Деплой на Heroku:
1. Создать приложение на Heroku.
2. Привязать аккаунт к Github.
    * файл requirements.txt содержит зависимости проекта.
    * Procfile - файл запуска, одна строка "_bot: python3 devman_bot.py_"
3. Задеплоить через Github.
4. Создать Config Vars. Все переменные окружения из .env файла записать в Config Vars. В коде вместо os.getenv('var')
использовать os.environ['var']

Есть возможность поменять текст уведомления. Используйте класс Message. В Message.header должны быть указаны места для
вставки названия урока и ссылки на сам урок. Данные подставятся автоматически с помощью метода строк _format_

Пример:
```python
header = 'У вас проверили работу "{}"\n\nСсылка на задачу: https://dvmn.org{}\n\n'
```

## Пример сообщения :
![Alt Text](http://ipic.su/img/img7/fs/Screenshot_20190430-173842.1556635709.png)
