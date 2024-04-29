import random


def generate_sms_code():
    """Функция генерации смс кодов."""
    sms_code = random.randint(1000, 9999)
    return sms_code

def send_sms_code(phone_number, confirmation_code):
    """Отправка СМС. Иммитация."""
    message = f'Код авторизации: {confirmation_code}'
    print(message)