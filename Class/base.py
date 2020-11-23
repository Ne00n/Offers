#!/usr/bin/python3
from selenium import webdriver
from fake_useragent import UserAgent
from pathlib import Path
from random import randint
import time, json, re, os

class Base:
    def __init__(self):
        self.selenium()

    def selenium(self):
        global browser
        print("Staring Selenium")
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
        wait = randint(7,80)
        print("Getting",url)
        browser.get(url)
        print("Waiting",wait,"seconds")
        time.sleep(wait)
        return browser.page_source

    def close(self):
        browser.close()

    def lowendbox(self):
        count,src = 1,"https://lowendbox.com/post-sitemap"
        dataDir = os.getcwd()+"/src/lowendbox/posts/"

        while True:
            print("Checking Sitemap")
            if not os.path.exists(dataDir):
                os.makedirs(dataDir)
            response = self.fetch(src+str(count)+".xml")
            urls = re.findall("href=\"(https:\/\/lowendbox.com\/blog/(.*?)\/)\">",response, re.MULTILINE)
            for url in urls:
                file = dataDir+url[1]+".json"
                if not Path(file).is_file():
                    response = self.fetch(url[0])
                    post = re.findall("(<div class=\"post-([0-9]+) post.*?\>.*?feedback\"></div></div>)",response, re.MULTILINE | re.DOTALL)
                    data = {'id':post[0][1],'post':post[0][0]}
                    with open(file, 'w') as f:
                        json.dump(data, f)
                else:
                    print("Skipping",url[1])
            count = count +1

    def vanilla(self,cat,site):
        currentOffers,count,src = "",1,"https://"+site+".com/categories/"+cat+"/p"
        dataDir = os.getcwd()+"/src/"+site+"/"+cat+"/"

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
