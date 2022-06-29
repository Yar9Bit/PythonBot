import telebot


from extension import ConvertException, ConvertValues
from config import TOKEN, keys

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def m(message: telebot.types.Message):
    text = '<Введите имя валюты> <В какую валюту перевести> <Количество переводимой валюты>\n '' \
Пользователь может получить список доступных валют /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        value = message.text.split(' ')

        if len(value) > 3:
            raise ConvertException('Слишком много параметров')
        elif len(value) < 3:
            raise ConvertException('Слишком мало параметров')
        quote, base, amount = value
        total_base = ConvertValues.get_price(quote, base, amount)
    except ConvertException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()
