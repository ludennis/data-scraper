#!/usr/bin/python3.7

import threading
import time

import concurrent.futures

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def ScrapeURL(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("window-size=1920,1080")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    return WebDriverWait(driver, 10).until(EC.visibility_of_element_located( \
      (By.CLASS_NAME, 'shopee-search-item-result__item')))


if __name__ == '__main__':
    urls = [
      'https://shopee.tw/ASUS-%E8%8F%AF%E7%A2%A9-DUAL-GTX1070-O8G-%E9%A1%AF%E7%A4%BA%E5%8D%A1-%E4%B9%9D%E6%88%90%E6%96%B0-i.118005626.2027799993',
      'https://shopee.tw/%E7%AC%AC%E4%B9%9D%E4%BB%A3i5%E4%B8%AD%E9%9A%8ERGB%E9%9B%BB%E7%AB%B6%E6%A9%9F(GTX1060-1070-1660-1650%E3%80%813A%E5%A4%A7%E4%BD%9C%E3%80%81LOL%E3%80%81PUBG%E5%90%83%E9%9B%9E-%E5%8F%83%E8%80%83)-i.106292453.6060080151',
      'https://shopee.tw/%E8%AA%A0%E6%94%B6GTX%E6%88%96RTX%E7%9A%84%E4%B8%80%E5%BC%B5%EF%BC%88%E5%85%A7%E8%A9%B3%EF%BC%89%EF%BC%81RTX2060S~2060%E6%88%96-gtx1080-1070-1660%E7%AD%89..-i.192228590.5657855285'
    ]

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("window-size=1920,1080")

    numThreads = 2

    with concurrent.futures.ThreadPoolExecutor(max_workers=numThreads) as executor:
        # start the load operations and mark each future with its url
        future_to_url = {executor.submit(ScrapeURL, url): url for url in urls}
        for future in concurrent.futures.as_completed(future_to_rul):
            url = future_to_url[future]
            try:
                element = future.result()
            except Exception as e:
                print("%r generated an exception: %s" % (url, e))
            else:
                print("scraped url: %r" % (url))

    print("Exiting main thread")
