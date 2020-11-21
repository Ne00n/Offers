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

    def close(self):
        browser.close()

    def getProviders(self,cat,site):
        dataDir = os.getcwd()+"/data/"+site+"/"+cat+"/"
        files = os.listdir(dataDir)
        providers = []
        for file in files:
            with open(dataDir+file, 'r') as f:
                data = json.load(f)
            if not data['user'] in providers:
                providers.append(data['user'])
        with open(os.getcwd()+"/data/"+site+"/providers.json", 'w') as f:
            json.dump(providers, f)

    def vanilla(self,cat,site):
        currentOffers,count,src = "",1,"https://"+site+".com/categories/"+cat+"/p"
        dataDir = os.getcwd()+"/data/"+site+"/"+cat+"/"

        print("Checking",site)
        response = self.fetch("https://"+site+".com")
        if "Cloudflare" in response:
            print("Failed to bypass CF")
            browser.close()
            return False

        while True:

            print("Getting",cat)
            response = self.fetch(src+str(str(count)+".json"))
            rawJson = re.sub('<[^<]+?>', '', response)
            try:
                currentOffers = json.loads(rawJson)
            except ValueError as e:
                print("Failed to parse json")
                return False

            if "Code" in currentOffers:
                print("End of line")
                return True

            print("Checking",cat)
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
