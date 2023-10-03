import re
import requests
from bs4 import BeautifulSoup

# Регулярное выражение для поиска номеров телефонов
PHONE_REGEX = re.compile(r'\b8\d{10}\b|\b\d{10}\b|\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b|\b\d{4}[-.\s]?\d{2}[-.\s]?\d{2}\b')

def fetch_phone_numbers(url):
    """
    Извлекает номера телефонов из веб-страницы.
    
    Parameters:
        url (str): URL веб-страницы для скрапинга.
    
    Returns:
        list of str: Список найденных номеров телефонов.
    """
    try:
        # Отправка HTTP-запроса и получение ответа
        response = requests.get(url)
        response.raise_for_status()  # проверить, успешен ли запрос
        
        # Парсинг HTML-кода страницы
        soup = BeautifulSoup(response.text, 'html.parser')
        text_content = soup.get_text(" ", strip=True)  # Извлечение текста из HTML
        
        # Поиск всех номеров телефонов на странице
        phone_numbers_raw = re.findall(PHONE_REGEX, text_content)
        
        # Очистка и форматирование номеров телефонов
        phone_numbers = [re.sub(r'\D', '', number) for number in phone_numbers_raw]  
        
        # Добавление префикса "8" для московских номеров, если он отсутствует
        phone_numbers = ['8' + number if len(number) == 10 else number for number in phone_numbers]
        
        return phone_numbers
    
    except requests.RequestException as e:
        print(f"Ошибка запроса: {e}")
        return []
    except Exception as e:
        print(f"Ошибка: {e}")
        return []

# Пример использования
url_example_1 = "https://hands.ru/company/about"
url_example_2 = "https://repetitors.info"

print(fetch_phone_numbers(url_example_1))
print(fetch_phone_numbers(url_example_2))