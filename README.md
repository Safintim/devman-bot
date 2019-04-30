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

## Зависимости
* *python-dotenv==0.10.1*
* *requests==2.21.0*
* *python-telegram-bot==11.1.0*

## Как использовать: 
Запустить скрипт:
```sh
python3 devman_bot.py
```

Найти бота в телеграме **_@devvm_bot_**

## Пример сообщения :
![Alt Text](http://ipic.su/img/img7/fs/Screenshot_20190430-173842.1556635709.png)
