import os
import random
import time

import environ
from selenium import webdriver
from selenium.common.exceptions import (ElementClickInterceptedException,
                                        UnexpectedAlertPresentException)
from selenium.webdriver.common.by import By

# Получение данных из переменных окружения
ENV = environ.Env()
COUNT_FOLDER_BACK = 1
current_dir = environ.Path(__file__) - COUNT_FOLDER_BACK
ENV.read_env(os.path.join(current_dir, '.env'))
EMAIL = ENV.str('EMAIL', 'my_email@my_email.ru')
PASS = ENV.str('PASS', 'the-best-pass')

# Инициализация драйвера
browser = webdriver.Chrome()


def delay(func):
    """Декоратор для дополнительного ожидания."""
    def wrapper(*args, **kwargs):
        time.sleep(random.uniform(.5, 2))
        return func(*args, **kwargs)
    return wrapper


@delay
def find_item(method, pattern, source=browser):
    return source.find_element(method, pattern)


@delay
def find_items(method, pattern):
    return browser.find_elements(method, pattern)


@delay
def check_access_enter(url):
    # Нажатие кнопки войти
    if browser.current_url == url:
        browser.switch_to.default_content()
        push_but = find_item(
            By.CSS_SELECTOR, '#form-login > div:nth-child(7) > button')
        push_but.click()
        return push_but


@delay
def check_aria_checked(captcha_checkbox):
    try:
        result = captcha_checkbox.get_attribute("aria-checked") == 'true'
    except (
            ElementClickInterceptedException, UnexpectedAlertPresentException):
        result = False
    finally:
        return result


@delay
def form_filling(url):
    # Открытие веб-страницы
    browser.get(url)

    # Поиск и нажатие на кнопку войти
    find_item(By.XPATH, '/html/body/div[1]/header/div/ul[2]/li[2]/a').click()

    # Ввод email в форму аутентификации
    email = find_item(By.CSS_SELECTOR, '.input-group > input[name=\'email\']')
    email.send_keys(EMAIL)

    # Ввод password в форму аутентификации
    find_item(By.ID, 'login-password').send_keys(PASS)

    # Активации чекпоинта 'Я не робот'
    frames = find_items(By.TAG_NAME, 'iframe')
    browser.switch_to.frame(frames[0])
    captcha_checkbox = find_item(By.CSS_SELECTOR, '#recaptcha-anchor')
    captcha_checkbox.click()

    # Время для ввода капчи
    while True:
        if check_aria_checked(captcha_checkbox):
            if check_access_enter(url):
                break
        continue
    return True


@delay
def print_result():

    # Получение таблицы
    proxys = find_items(
        By.XPATH,
        '/html/body/div[1]/div[2]/div/div/div/div/div[2]/table/tbody/tr'
    )

    # Извлечение информации из таблицы и печать.
    for proxy in proxys[1:-2]:
        proxy_ip = find_item(By.CSS_SELECTOR, '.right.clickselect > b', proxy)
        deadline = find_item(
            By.CSS_SELECTOR,
            'td:nth-child(4) > ul > li:nth-child(1) > div.right.color-success',
            proxy
        )

        print(f'{proxy_ip.text} - {deadline.text}')


def main(url):
    while True:
        if form_filling(url):
            break
    print_result()


if __name__ == "__main__":

    # Ресурс для парсинга
    url = 'https://proxy6.net/'
    main(url)

    # Закрытие браузера
    browser.quit()
