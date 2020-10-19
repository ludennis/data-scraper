#!/usr/bin/python3

from selenium import webdriver
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

    item_list = WebDriverWait(driver, 10).until(EC.visibility_of_element_located( \
      (By.XPATH, "//div[contains(@class, 'shopee-search-item-result__items')]")))

    print("Finished Waiting")

    items = item_list.find_elements_by_class_name('shopee-search-item-result__item')

    for item in items:
        name = item.find_element_by_xpath('//div[@data-sqe="name"]//div')
        print(name.text)

  return 0
