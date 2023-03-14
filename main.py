import json

import requests
import telebot

TOKEN = '6075939547:AAH12b2M57oBPTWx5PBcihRv2bWnNMoz1wM'
bot = telebot.TeleBot(TOKEN)

keys_v = {
    'биткоин': 'BTC',
    'эфириум': 'ETH',
    'доллар': 'USD',
    'рубль': 'RUB',
    'евро': 'EUR'
}

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду, в следующем формате: \n <имя валюты>  \
<в какую валюту перевести> \
<количество переводимой валюты>\n Увидеть список всех доступных валют: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message):
    text = 'Доступные валюты'
    for key in keys_v.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert_v(message):
    # биткоин доллар 10
    quote, base, amound = message.text.split(' ')
    # получаем курс через АРI
    r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={keys_v[quote]}&tsyms={keys_v[base]}')
    # сохраняем курс в переменную
    total = float((json.loads(r.content)[keys_v[base]]))
    # множим на количество едениц и округляем
    total_base = round((total * float(amound)), 4)
    #выводим пользователю
    text = f'Цена {amound} {quote} в {base} = {total_base}'
    bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
