import os
import pickle
import random
import time

import environ
from selenium import webdriver
from selenium.webdriver.common.by import By

# Создание environment variables
# рекомендуется рядом с текущим файлом создать .env файл, в котором указать
# действительные EMAIL и PASS(password), перечислить в формате ключ=значение
# без пробелов до и после знака ровно, значения указываются без кавычек
ENV = environ.Env()
COUNT_FOLDER_BACK = 1
current_dir = environ.Path(__file__) - COUNT_FOLDER_BACK
ENV.read_env(os.path.join(current_dir, ".env"))
EMAIL = ENV.str('EMAIL', 'my_email@my_email.ru')
PASS = ENV.str('PASS', 'the-best-pass')

# Ресурс для парсинга
URL = 'https://proxy6.net/'


def delay():
    time.sleep(random.uniform(.5, 2))


# Инициализация драйвера
browser = webdriver.Chrome()

# Открытие веб-страницы
browser.get(URL)

# загрузка куки
for cookie in pickle.load(open('session', 'rb')):
    browser.add_cookie(cookie)
print('Куки загружены')
delay()

# Переход на страницу "Прокси"
browser.get('https://proxy6.net/user/proxy')
delay()

# Получение таблицы
table_body = '/html/body/div[1]/div[2]/div/div/div/div/div[2]/table/tbody/tr'
proxys = browser.find_elements(By.XPATH, table_body)

# Извлечение информации из таблицы и печать.
for proxy in proxys[1:-2]:
    select_ip = '.right.clickselect > b'
    proxy_ip = proxy.find_element(By.CSS_SELECTOR, select_ip).text

    select_deadline = (
        'td:nth-child(4) > ul > li:nth-child(1) > div.right.color-success')
    deadline = proxy.find_element(By.CSS_SELECTOR, select_deadline).text

    print(f'{proxy_ip} - {deadline}')

# Закрытие браузера
browser.quit()
