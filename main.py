import telebot
from config import TOKEN, keys_v
from extensions import Converter, ConvertionException, get_keyboard


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help']) #выводим описание работы бота
def help(message: telebot.types.Message):
    markup = get_keyboard()
    text = 'Чтобы начать работу введите команду, в следующем формате: \n <имя валюты>  \
<в какую валюту перевести> \
<количество>\n. Увидеть список всех доступных валют: /values'
    bot.reply_to(message, text, reply_markup=markup)


@bot.message_handler(commands=['values']) # список доступных валют
def values(message):
    markup = get_keyboard()
    text = 'Доступные валюты:'
    for key in keys_v.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text, reply_markup=markup)


@bot.message_handler(content_types=['text']) # конвертация валют
def convert_v(message):
    markup = get_keyboard()
    try:
        value = message.text.split(' ')
        if len(value) != 3:
            raise ConvertionException('Введите 3 параметра!')
        # вал1 вал2 количество
        quote, base, amount = value
        total_base = Converter.get_prise(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя! \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду!\n{e}')
        # выводим пользователю
    else:
        text = f'Цена {amount} {quote} = {total_base} {base}'
        bot.send_message(message.chat.id, text, reply_markup=markup)


bot.polling()
