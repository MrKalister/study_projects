import pickle
import time

from selenium import webdriver

URL = 'https://proxy6.net/'
browser = webdriver.Chrome()
browser.get(URL)

time.sleep(100)
pickle.dump(browser.get_cookies(), open('session', 'wb'))
print('Куки сохранены')
browser.quit()
