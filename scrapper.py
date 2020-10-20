#!/usr/bin/python3

from time import sleep

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from psql_utils import InitializePostgreSQLDatabase

if __name__ == '__main__':
    InitializePostgreSQLDatabase(user='d400')

    keyword = 'gtx1070'
    url = 'https://shopee.tw/search?keyword={}&noCorrection=true' \
      '&page=0&sortBy=ctime&usedItem=true'.format(keyword)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("window-size=1920,1080")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    driver_tab = webdriver.Chrome(options=chrome_options)

    WebDriverWait(driver, 10).until(EC.visibility_of_any_elements_located( \
      (By.CLASS_NAME, 'shopee-search-item-result__item')))

    height = driver.execute_script("return document.documentElement.scrollHeight")
    i = 0
    while i < height:
        height = driver.execute_script("return document.documentElement.scrollHeight")
        driver.execute_script("window.scrollTo(0, {});".format(i))
        i = i + 500
        sleep(0.5)


    items = WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located( \
      (By.CLASS_NAME, 'shopee-search-item-result__item')))

    print("number of items: {}".format(len(items)))

    for i, item in enumerate(items):
        try:
            name = item.find_element_by_xpath('.//div[@data-sqe="name"]//div').text
            price = item.find_element_by_xpath('.//div/a/div/div[2]/div[2]/div/span[2]').text
            product_link = item.find_element_by_xpath('.//div/a').get_attribute('href')

            driver_tab.get(product_link)
            product_detail = WebDriverWait(driver_tab, 10).until(EC.visibility_of_element_located( \
              (By.CLASS_NAME, 'page-product__detail')))
            description = product_detail.find_element_by_xpath('.//div[2]/div[2]/div/span').text

            print("{}. {} => ${} \n{}\n".format(i, name, price, \
              product_link))
        except NoSuchElementException:
            pass

