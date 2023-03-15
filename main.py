import telebot
from config import TOKEN, keys_v
from extensions import Converter, ConvertionException
from telebot import types


bot = telebot.TeleBot(TOKEN)


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
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert_v(message):
    try:
        value = message.text.split(' ')

        if len(value) != 3:
            raise ConvertionException('Введите 3 параметра')

        # вал1 вал2 количество
        quote, base, amount = value
        total_base = Converter.get_prise(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя. \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
        # выводим пользователю
    else:
        text = f'Цена {amount} {quote} = {total_base} {base}'
        bot.send_message(message.chat.id, text)


bot.polling()
