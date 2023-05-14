import requests
from bs4 import BeautifulSoup
from time import sleep

import telebot

TOKEN = '' # BOT TOKEN
MAIN_ID = 0 # The ID where bot will send the message
bot = telebot.TeleBot(TOKEN)

url = "https://kzn.besposrednika.ru/"
headers = {
    "accept": '*/*',
    'User-agent': '...'
}

def shearing(prod, case):
    result = prod.split()
    final = ""
    if case == 0:
        for i in result:
            if i != 'Сегодня' and i != 'в':
                final += i + " "
        return final.strip()
    if case == 1:
        for i in result:
            final += i + " "
        return final.strip()

date_2 = ""
while True:
    req = requests.get(url, headers=headers)
    src = req.text

    soup = BeautifulSoup(src, 'lxml')
    date_href = soup.find(class_="sEnLiDate today")

    date_1 = shearing(date_href.text, 0)

    if date_1 != date_2:
        new_href = soup.find(class_="sEnLiTitle")
        location = soup.find(class_="map-marker")

        url_new = new_href.find('a').get('href')

        bot.send_message(MAIN_ID, f'На сайте размешено новое объявление в {date_1}: {shearing(new_href.text, 1)}\n'
                                  f'{shearing(location.text, 1)}\n'
                                  f'{url_new}')
        date_2 = shearing(date_href.text, 0)
    else:
        sleep(30)