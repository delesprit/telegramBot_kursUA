
import telebot
import requests
import json
import os
import time
from datetime import datetime
now = datetime.now()
bot = telebot.TeleBot('XXXXXXXX') #API-Key

now_time = now.strftime("%I:%M %d.%m.%y") #текущее вермя + дата

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Старт-бот', reply_markup=keyboard1)

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.from_user.id, 'Это Помощь aga')

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text.lower() == 'курс валют':
        bot.send_message(message.from_user.id, text_kurs, parse_mode="Markdown", reply_markup=keyboard1)


# mono банит за частые запросы, необходимо кеширование
def parser_mono():
    if ( int(time.time()) - 1000 > os.path.getmtime('mono.json') ):
        link_mono = requests.get('https://api.monobank.ua/bank/currency')
        file = open('mono.json', 'w')
        file.write(link_mono.text)
        file.close()
        print("парсим")
    else:
        print("не парсим")


#Privat
link_privat = requests.get('https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5')
result_privat = json.loads(link_privat.text)
#usd
usdBuy_privat = format(float(result_privat[0]['buy']), '.2f')
usdSale_privat = format(float(result_privat[0]['sale']), '.2f')
#eur
eurBuy_privat = format(float(result_privat[1]['buy']), '.2f')
eurSale_privat = format(float(result_privat[1]['sale']), '.2f')
#rur
rurBuy_privat = format(float(result_privat[2]['buy']), '.2f')
rurSale_privat = format(float(result_privat[2]['sale']), '.2f')

#Mono
parser_mono()
file = open("mono.json", "r")
link_mono = file.read()
file.close()
result_mono = json.loads(link_mono)
#usd
usdBuy_mono = format(float(result_mono[0]['rateBuy']), '.2f')
usdSale_mono = format(float(result_mono[0]['rateSell']), '.2f')
#eur
eurBuy_mono = format(float(result_mono[1]['rateBuy']), '.2f')
eurSale_mono = format(float(result_mono[1]['rateSell']), '.2f')
#rur
rurBuy_mono = format(float(result_mono[2]['rateBuy']), '.2f')
rurSale_mono = format(float(result_mono[2]['rateSell']), '.2f')

#НБУ
link_nbu = requests.get('https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json')
result_nbu = json.loads(link_nbu.text)
#usd
usd_nbu = format(float(result_nbu[26]['rate']), '.2f')
#eur
eur_nbu = format(float(result_nbu[33]['rate']), '.2f')
#rur
rur_nbu = format(float(result_nbu[18]['rate']), '.2f')



text_kurs = 'Курс валют на ' + now_time + '\n' \
            '\n' \
            '***USD:***\n' \
            'НБУ              ' + usd_nbu + '\n' \
            'Моно      ' + usdBuy_mono + ' | ' + usdSale_mono + '\n' \
            'Приват   ' + usdBuy_privat + ' | ' + usdSale_privat + '\n' \
            '\n' \
            '***EUR:***\n' \
            'НБУ              ' + eur_nbu + '\n' \
            'Моно      ' + eurBuy_mono + ' | ' + eurSale_mono + '\n' \
            'Приват   ' + eurBuy_privat + ' | ' + eurSale_privat + '\n' \
            '\n' \
            '***RUR:***\n' \
            'НБУ              ' + rur_nbu + '\n' \
            'Моно      ' + rurBuy_mono + ' | ' + rurSale_mono + '\n' \
            'Приват   ' + rurBuy_privat + ' | ' + rurSale_privat + '\n' \
            '\n' \


keyboard1 = telebot.types.ReplyKeyboardMarkup(True)
keyboard1.row('/start')
keyboard1.row('Курс валют', 'Пока')


bot.polling(none_stop=True)

