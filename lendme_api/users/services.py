import requests

import random
import os
from dotenv import load_dotenv

load_dotenv()


def generate_sms_code():
    """Функция генерации смс кодов."""
    sms_code = random.randint(10000, 99999)
    return sms_code

def send_sms_code(phone_number, confirmation_code):
    """Отправка СМС. Иммитация."""
    message = f'Код авторизации: {confirmation_code}'
    print(message)

    # """Отправка СМС через sms.ru."""
    # api_id = os.getenv('SMSRU_API_ID')
    # sms_api_url = 'https://sms.ru/sms/send'
    #
    # params = {
    #     'api_id': api_id,
    #     'to': phone_number,
    #     'msg': f'Код авторизации: {confirmation_code}',
    #     'json': 1
    #
    # }
    #
    # response = requests.get(sms_api_url, params=params)
    # if response.status_code == 200:
    #     result = response.json()
    #     if result.get('status') == 'OK':
    #         print('Сообщение успешно отправлено')
    #     else:
    #         print(f'Ошибка при отправке сообщения: {result.get("status_code")}')
    # else:
    #     print('Ошибка при отправке запроса')