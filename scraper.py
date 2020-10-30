#!/usr/bin/python3

from time import sleep

import concurrent.futures

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


def ScrapeShopeeItemDetails(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("window-size=1920,1080")
    driver = webdriver.Chrome(options=chrome_options)
    try:
        driver.get(url)
        print("Scraping url: {}".format(url))
        product_detail = WebDriverWait(driver, 10).until(EC.visibility_of_element_located( \
          (By.CLASS_NAME, 'page-product__detail')))

        details = product_detail.find_elements_by_xpath('.//div[1]/div[2]/*')
        for detail in details:
            if detail.find_element_by_xpath('.//label').text == '品牌':
                brand = detail.find_element_by_xpath('.//a').text
            elif detail.find_element_by_xpath('.//label').text == '庫存':
                quantity = detail.find_element_by_xpath('.//div').text
            elif detail.find_element_by_xpath('.//label').text == '出貨地':
                location = detail.find_element_by_xpath('.//div').text
        description = product_detail.find_element_by_xpath('.//div[2]/div[2]/div/span').text
    except NoSuchElementException:
        print("No such element exception")
        pass

    return {'brand': brand, 'quantity': quantity, 'location': location, 'description': description}


if __name__ == '__main__':
    numThreads = 24

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

    # TODO: combine these scraping together
    with concurrent.futures.ThreadPoolExecutor(max_workers=numThreads) as executor:
        future_to_shopee_item = { \
          executor.submit(ScrapeShopeeItemDetails, shopee_item.url): shopee_item \
          for shopee_item in shopee_items}
        for future in concurrent.futures.as_completed(future_to_shopee_item):
            shopee_item = future_to_shopee_item[future]
            try:
                details = future.result()
            except Exception as e:
                print("%r generated as exception: %s" % (shopee_item.url, e))
            else:
                print("scraped url: %r" % (url))
                shopee_item.brand = details['brand']
                shopee_item.quantity = details['quantity']
                shopee_item.location = details['location']
                shopee_item.description = details['description']

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
