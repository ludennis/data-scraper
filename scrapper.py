#!/usr/bin/python3

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

if __name__ == '__main__':
    url = 'https://shopee.tw/search?keyword=nvidia'

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    items = WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located( \
      (By.CLASS_NAME, 'shopee-search-item-result__item')))

    print("number of items: {}".format(len(items)))

    for i, item in enumerate(items):
        try:
            name = item.find_element_by_xpath('.//div[@data-sqe="name"]//div')
            print("{}. {}".format(i, name.text))
        except NoSuchElementException:
            pass

