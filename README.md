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

Скрипт берет настройки из Config Vars, где указаны токен девмана, токен чат-девман-бота, 
токен чат-логгер-бота и номер чата. Если запускать локально, то создайте .env файл с настройками.
 Загрузите .env с помощью функции load_dotenv и получите данные с помощью os.getenv.
 
Пример .env файла 
```sh
TOKEN_DEVMAN=your_token
TOKEN_DEVMAN_BOT=your_token
TOKEN_LOGGER_BOT=your_token
CHAT_ID=your_chat_id
```

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

## Комментарии:
Есть возможность поменять текст уведомления. Используйте класс Message. В Message.header должны быть указаны места для
вставки названия урока и ссылки на сам урок. Данные подставятся автоматически с помощью метода строк _format_

Пример:
```python
header = 'У вас проверили работу "{}"\n\nСсылка на задачу: https://dvmn.org{}\n\n'
is_positive_result = 'Все замечательно, можно приступать к следующей задаче'
is_negative_result = 'Преподаватель нашел ошибки..'
bottom = 'Вперед!'
message = Messsage(header, is_positive_result, is_negative_result, bottom)

BotDevman(LogsHandler, message=message).run()
```

Есть возможность не использовать логгер-бота или использовать своего, для этого нужно написать свой обработчик логов.

Пример:
```python
class MyHandler(logging.Handler):

    def __init__(self,):
        super().__init__()
        self.bot = MyBotLogger()

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_report(log_entry)
```

## Пример сообщения :
![Alt Text](http://ipic.su/img/img7/fs/Screenshot_20190430-173842.1556635709.png)
![Alt Text](http://ipic.su/img/img7/fs/Screenshot_20190510-121011_2.1557479765.png)