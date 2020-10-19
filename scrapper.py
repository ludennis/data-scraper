#!/usr/bin/python3

from time import sleep

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

if __name__ == '__main__':
    url = 'https://shopee.tw/search?keyword=nvidia'

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("window-size=1920,1080")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    WebDriverWait(driver, 10).until(EC.visibility_of_any_elements_located( \
      (By.CLASS_NAME, 'shopee-search-item-result__item')))

    height = driver.execute_script("return document.documentElement.scrollHeight")
    i = 0
    while i < height:
        print("i = {}".format(i))
        height = driver.execute_script("return document.documentElement.scrollHeight")
        print("height = {}".format(height))
        driver.execute_script("window.scrollTo(0, {});".format(i))
        i = i + 500
        sleep(0.5)


    items = WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located( \
      (By.CLASS_NAME, 'shopee-search-item-result__item')))

    print("number of items: {}".format(len(items)))

    for i, item in enumerate(items):
        try:
            name = item.find_element_by_xpath('.//div[@data-sqe="name"]//div')
            print("{}. {}".format(i, name.text))
        except NoSuchElementException:
            pass

