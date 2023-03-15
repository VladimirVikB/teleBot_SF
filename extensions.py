import json
import requests
from config import keys_v

class ConvertionException(Exception):
    pass


class Converter:
    @staticmethod
    def get_prise(quote: str, base: str, amount: float):
        if quote == base:
            raise ConvertionException(f'{quote}, введен дважды. Для конвертации введите разные валюты!')

        try:
            quote_mark = keys_v[quote]
        except KeyError:
            raise ConvertionException(f'Введенная валюта {quote} не обрабатывается!')
        try:
            base_mark = keys_v[base]
        except KeyError:
            raise ConvertionException(f'Введенная валюта {base} не обрабатывается!')
        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Неверный ввод {amount}. Введите цифры!')
        # получаем курс через АРI
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_mark}&tsyms={base_mark}')
        # множим курс на количество и сохраняем курс в переменную
        total = (json.loads(r.content)[keys_v[base]]) * amount
        return total
