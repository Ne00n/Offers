#!/usr/bin/python3
from selenium import webdriver
from fake_useragent import UserAgent
from pathlib import Path
from random import randint
import time, json, re, os

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
        time.sleep(randint(7,30))
        return browser.page_source

    def let(self):
        currentOffers,count,src = "",1,"https://www.lowendtalk.com/categories/offers/p"
        dataDir = os.getcwd()+"/data/lowendtalk/"

        print("Checking Lowendtalk")
        response = self.fetch("https://lowendtalk.com")
        if "Cloudflare" in response:
            print("Failed to bypass CF")
            browser.close()
            return False

        while True:

            print("Getting Offers")
            response = self.fetch(src+str(str(count)+".json"))
            rawJson = re.sub('<[^<]+?>', '', response)
            try:
                currentOffers = json.loads(rawJson)
            except ValueError as e:
                print("Failed to parse json")
                break

            if "Code" in currentOffers:
                print("End of line")
                break

            print("Checking Offers")
            if not os.path.exists(dataDir):
                os.makedirs(dataDir)
            for discussion in currentOffers['Discussions']:
                file = dataDir+str(discussion['DiscussionID'])+"-"+discussion['FirstName']+".json"
                print("Checking",discussion['DiscussionID'])
                if not Path(file).is_file():
                    data = {'id':discussion['DiscussionID'],'date':discussion['DateInserted'],'user':discussion['FirstName'],'post':discussion['Body']}
                    with open(file, 'w') as f:
                        json.dump(data, f)
                else:
                    print(discussion['DiscussionID'],"already exist")
                    return True

            count = count +1

        browser.close()
