#!/usr/bin/python3

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

if __name__ == '__main__':
    url = 'https://shopee.tw/search?keyword=nvidia'

    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    main = driver.find_element_by_id('main')
    driver.quit()
