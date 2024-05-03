import requests

import random
import os
from dotenv import load_dotenv

from django.core.cache import cache
from django.core.mail import send_mail
from django.template.loader import get_template

load_dotenv()


def generate_sms_code():
    """Функция генерации смс кодов."""
    sms_code = random.randint(10000, 99999)
    return sms_code

def send_sms_code(phone_number, sms_code):
    """Отправка СМС. Иммитация."""
    message = f'Код авторизации: {sms_code}'
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


def send_confirmation_email(email, token_id, user_id):
    """Функция отправки токена по почте."""
    data = {
        'token_id': str(token_id),
        'user_id': str(user_id)
    }
    message = get_template('confirmation_email.txt').render(data)
    send_mail(
        subject='Пожалуйста, подтвердите адрес электронной почты',
        message=message,
        from_email='lendme46@gmail.com',
        recipient_list=[email],
        fail_silently=True
    )
