#!/usr/bin/python3
from selenium import webdriver
from fake_useragent import UserAgent
import time

class Base:
    def __init__(self):
        print("Staring Selenium")
        self.selenium()

    def selenium(self):
        global browser
        options = webdriver.ChromeOptions()
        ua = UserAgent()
        userAgent = ua.chrome
        print(userAgent)
        options.add_argument("--disable-blink-features")
        options.add_argument(f'user-agent={userAgent}')
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("start-maximized")
        options.add_argument("disable-infobars")
        options.add_argument("--disable-extensions")
        browser = webdriver.Chrome(options=options)

    def fetch(self,url):
        browser.get(url)
        time.sleep(7)
        return browser.page_source

    def let(self):
        print("Checking Lowendtalk")
        response = self.fetch("https://lowendtalk.com")
        print(response)
        browser.close()
