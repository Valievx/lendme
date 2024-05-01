import os
from dotenv import load_dotenv
from typing import Optional

import requests

from django.http import HttpRequest

load_dotenv()

API_URL = "https://api.ipgeolocation.io/ipgeo"
API_KEY = os.getenv("IPGEOLOCATION_API_KEY")


def get_client_ip(request: HttpRequest) -> Optional[str]:
    """
    Получает IP-адрес клиента из запроса и
    возвращает в правильном формате.

    Source: https://stackoverflow.com/a/4581997
    """

    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0]
    else:
        return request.META.get("REMOTE_ADDR")


def get_location_by_ip(ip_address):
    """
    Получение информации о местоположении по IP-адресу
    с использованием API IPGeolocation.
    """
    try:
        response = requests.get(
            API_URL,
            params={
                "apiKey": API_KEY,
                "ip": ip_address
            }
        )
        data = response.json()
        if response.status_code == 200:
            return {
                "city": data.get("city"),
            }
        else:
            print("Не удалось получить данные геолокации:", data.get("message"))
            return None
    except Exception as e:
        print("Возникло исключение при получении данных геолокации:", str(e))
        return None
