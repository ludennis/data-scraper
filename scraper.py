#!/usr/bin/python3

from time import sleep

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from psql_utils import ConnectDatabase
from psql_utils import InitializePostgreSQLDatabase
from psql_utils import InsertShopeeItem

import urllib.request

from models import ShopeeItem


if __name__ == '__main__':
    database_name = 'scraper_db'
    user_name = 'd400'
    engine = ConnectDatabase(user=user_name, db_name=database_name)
    print('Connected to database {} with user {}'.format(database_name, user_name))
    InitializePostgreSQLDatabase(engine)
    print('Database initialized')

    # TODO: look for a file containing a list of search phrases
    search_phrase = 'gtx1070'
    url = 'https://shopee.tw/search?keyword={}&noCorrection=true' \
      '&page=0&sortBy=ctime&usedItem=true'.format(search_phrase)
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
        height = driver.execute_script("return document.documentElement.scrollHeight")
        driver.execute_script("window.scrollTo(0, {});".format(i))
        i = i + 500
        sleep(0.5)

    items = WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located( \
      (By.CLASS_NAME, 'shopee-search-item-result__item')))

    print("number of items: {}".format(len(items)))

    shopee_items = []

    for i, item in enumerate(items):
        try:
            name = item.find_element_by_xpath('.//div[@data-sqe="name"]//div').text
            price = item.find_element_by_xpath('.//div/a/div/div[2]/div[2]/div/span[2]').text
            price = int(price.replace(',',''))
            product_url = item.find_element_by_xpath('.//div/a').get_attribute('href')
            image = item.find_element_by_xpath('.//div/a/div/div[1]/img')
            image_source = image.get_attribute("src")
            image_data = urllib.request.urlopen(image_source).read()

            shopee_items.append(
              ShopeeItem(name=name, price=price, search_phrase=search_phrase, url=product_url, \
                         image=image_data, seller=None, brand=None, quantity=None, location=None, \
                         description=None))
        except NoSuchElementException:
            print("No such element exception")
            pass

    for shopee_item in shopee_items:
        if shopee_item.url == None:
            print("No url found")
            continue
        try:
            print("Scraping url: {}".format(shopee_item.url))
            driver.get(shopee_item.url)
            product_detail = WebDriverWait(driver, 10).until(EC.visibility_of_element_located( \
              (By.CLASS_NAME, 'page-product__detail')))

            print("product_detail: {}".format(product_detail))
            details = product_detail.find_elements_by_xpath('.//div[1]/div[2]/*')
            for detail in details:
                if detail.find_element_by_xpath('.//label').text == '品牌':
                    shopee_item.brand = detail.find_element_by_xpath('.//a').text
                    print("Found brand = {}".format(shopee_item.brand))
                elif detail.find_element_by_xpath('.//label').text == '庫存':
                    shopee_item.quantity = detail.find_element_by_xpath('.//div').text
                    print("Found quantity = {}".format(shopee_item.quantity))
                elif detail.find_element_by_xpath('.//label').text == '出貨地':
                    shopee_item.location = detail.find_element_by_xpath('.//div').text
                    print("Found location = {}".format(shopee_item.location))
            shopee_item.description = \
              product_detail.find_element_by_xpath('.//div[2]/div[2]/div/span').text
            print("found description: {}".format(shopee_item.description))
        except NoSuchElementException:
            print("No such element exception")
            pass

    for shopee_item in shopee_items:
        if shopee_item.url == None:
            print("No url found")
            continue
        try:
            print("Scraping url: {}".format(shopee_item.url))
            driver.get(shopee_item.url)
            seller_detail = WebDriverWait(driver, 10).until(EC.visibility_of_element_located( \
              (By.CLASS_NAME, 'page-product__shop')))

            shopee_item.seller = seller_detail.find_element_by_xpath('.//div[1]/div/div[1]').text
            print("found seller = {}".format(shopee_item.seller))
        except NoSuchElementException:
            print("No such element exception")
            pass

    for shopee_item in shopee_items:
        InsertShopeeItem(engine, shopee_item)
        print("Inserted ShopeeItem {} to database".format(shopee_item.name))

    driver.quit()
