#!/usr/bin/python3
from pyvirtualdisplay import Display
from fake_useragent import UserAgent
from selenium import webdriver
from pathlib import Path
from random import randint
import time, json, os
import urllib.parse
import regex as re

class Base:

    headless,before = False,""

    def __init__(self,headless):
        self.headless = headless
        self.selenium()

    def selenium(self):
        global browser,display
        if self.headless:
            print("Starting virtual display")
            display = Display(visible=0, size=(1920, 1080))
            display.start()
        print("Starting Selenium")
        options = webdriver.ChromeOptions()
        try:
            ua = UserAgent()
            userAgent = ua.chrome
            print(userAgent)
            options.add_argument(f'user-agent={userAgent}')
        except Exception as e:
            print("Error",e)
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("start-maximized")
        options.add_argument("--disable-extensions")
        browser = webdriver.Chrome(options=options)
        browser.set_page_load_timeout(60)

    def fetch(self,url):
        wait,count = randint(7,60),0
        print("Getting",url)
        while count < 3:
            try:
                browser.get(url)
                print("Waiting",wait,"seconds")
                time.sleep(wait)
                return browser.page_source
            except Exception as e:
                print("Error",e)
                wait = randint(30,80)
                print("Waiting",wait,"seconds")
                time.sleep(wait)
            count = count +1
        return False

    def fatch(self,url):
        html = self.fetch(url)
        if self.detectCrash():
            html = self.fetch(url)
        if html == self.before:
            print("Browser does not seem to respond, restarting instance")
            self.restart()
            html = self.fetch(url)
        self.before = html
        return html

    def detectCrash(self):
        try:
            crashPrevention = browser.current_url
        except Exception as e:
            print("Error",e)
            print("Browser seems to have crashed")
            self.restart()
            return True

    def restart(self):
        try:
            self.close()
        except Exception as e:
            print("Error",e)
            print("Failed to close browser")
        self.selenium()
        print("Browser restarted")

    def close(self):
        browser.close()
        browser.quit()
        if self.headless:
            display.stop()

    def checkCF(self,html):
        count = 0
        if "Attention Required!" in html: count = count +1
        if "Cloudflare" in html: count = count +1
        if "Cloudflare Ray ID" in html: count = count +1
        if "CAPTCHA" in html: count = count +1
        if "Please turn JavaScript on and reload the page" in html: count = count +2
        if "Please stand by, while we are checking your browser" in html: count = count +2
        print("CF score",count)
        if count >= 5: return True

    def lowendbox(self):
        count,src = 1,"https://lowendbox.com/post-sitemap"
        dataDir = os.getcwd()+"/src/lowendbox/posts/"

        while True:
            print("Checking Sitemap")
            if not os.path.exists(dataDir):
                os.makedirs(dataDir)
            response = self.fetch(src+str(count)+".xml")
            if response == False: return False

            if "The Page you requested was not found" in response:
                print("End of line")
                return True

            urls = re.findall("href=\"(https:\/\/lowendbox.com\/blog/(.*?)\/)\">",response, re.MULTILINE)
            for url in urls:
                file = dataDir+urllib.parse.unquote(url[1])+".json"
                if not Path(file).is_file():
                    response = self.fetch(url[0])
                    if response == False: return False
                    post = re.findall("(<div class=\"post-([0-9]+) post.*?\>.*?feedback\"></div></div>)",response, re.MULTILINE | re.DOTALL)
                    try:
                        data = {'id':post[0][1],'post':post[0][0]}
                        with open(file, 'w') as f:
                            json.dump(data, f)
                    except:
                        print("Skipping",url[1],"regex error")
                else:
                    print("Skipping",url[1])
            count = count +1

    def discourseGetCreator(self,users,topic):
        for poster in topic['posters']:
            for user in users:
                if poster['user_id'] == user['id'] and "Original Poster" in poster['description']:
                    return user['id'],user['username']

    def discourse(self,cat,site):
        currentOffers,count = "",0
        dataDir,scans = os.getcwd()+"/src/"+site+"/"+cat+"/",0

        print("Checking",site)
        response = self.fetch("https://"+site)
        if response == False: return False
        if self.checkCF(response):
            print("Failed to bypass CF")
            return False

        while True:

            print("Getting",cat)
            response = self.fetch("https://"+site+"/c/"+cat+".json?page="+str(count))
            if response == False: return False
            rawJson = re.sub('<[^<]+?>', '', response)

            try:
                currentOffers = json.loads(rawJson)
            except ValueError as e:
                print("Failed to parse json")
                return False

            if not currentOffers['topic_list']['topics']:
                print("End of line")
                return True

            print("Getting",cat)
            if not os.path.exists(dataDir):
                os.makedirs(dataDir)
            for topic in currentOffers["topic_list"]["topics"]:
                creatorID,creator = self.discourseGetCreator(currentOffers['users'],topic)
                file = dataDir+str(topic['id'])+"-"+creator+".json"
                print("Checking",topic['id'])
                if not Path(file).is_file():
                    response = self.fetch("https://"+site+"/t/"+str(topic['id'])+".json")
                    if response == False: return False
                    rawJson = re.sub('<[^<]+?>', '', response)
                    try:
                        currentPost = json.loads(rawJson)
                    except ValueError as e:
                        print("Failed to parse json")
                        return False
                    posts = currentPost['post_stream']['posts']
                    data = {'id':topic['id'],'date':posts[0]['created_at'],'user':posts[0]['username'],'post':posts[0]['cooked']}
                    with open(file, 'w') as f:
                        json.dump(data, f)
                else:
                    print(topic['id'],"already exist")
                    scans = scans +1
                    if scans == 20:
                        return True

            count = count +1

    def vBulletin(self,cat,site):
        currentOffers,count = "",1
        dataDir,scans = os.getcwd()+"/src/"+site+"/"+cat+"/",0

        print("Checking",site)
        response = self.fetch("https://"+site)
        if response == False: return False
        if self.checkCF(response):
            print("Failed to bypass CF")
            return False

        while True:

            print("Getting",cat)
            response = self.fetch("https:/"+site+"/"+cat+f"/&page={count}&sort=threadstarted")
            if response == False: return False
            if self.checkCF(response):
                print("Failed to bypass CF")
                return False

            urls = re.findall('threadbit.*?href=\"(showthread\.php\?t=([\d]+)).*?Started by (.*?) on',response, re.MULTILINE | re.DOTALL)
            for url in urls:

                print("Getting",cat)
                if not os.path.exists(dataDir):
                    os.makedirs(dataDir)
                file = dataDir+url[1]+"-"+url[2]+".json"
                print("Checking",url[0])
                if not Path(file).is_file():
                    response = self.fetch("https://"+site+"/"+url[0])
                    if response == False: return False
                    post = re.findall('postbit postbitim .*?date\">([\d-]+|Today),.*?postcontent(.*?)\class=\"postfoot\">',response, re.DOTALL | re.MULTILINE)
                    data = {'id':url[1],'date':post[0][0],'user':url[2],'post':post[0][1]}
                    with open(file, 'w') as f:
                        json.dump(data, f)
                else:
                    print(url[1],"already exist")
                    scans = scans +1
                    if scans == 20:
                        return True

            count = count +1

    def xenforo(self,cat,site):
        currentOffers,count = "",1
        dataDir,scans = os.getcwd()+"/src/"+site+"/"+cat+"/",0

        print("Checking",site)
        response = self.fetch("https://"+site)
        if response == False: return False
        if self.checkCF(response):
            print("Failed to bypass CF")
            return False

        while True:

            print("Getting",cat)
            response = self.fetch("https:/"+site+"/forums/"+cat+"/page-"+str(count))
            if response == False: return False
            if self.checkCF(response):
                print("Failed to bypass CF")
                return False

            urls = re.findall('<li><a href="\/members\/([a-z-]*)\.[0-9]+.*?href="(\/threads\/.*?.\.([0-9]+))\/"',response, re.MULTILINE | re.DOTALL)
            for url in urls:

                print("Getting",cat)
                if not os.path.exists(dataDir):
                    os.makedirs(dataDir)
                file = dataDir+url[2]+"-"+url[0]+".json"
                print("Checking",url[2])
                if not Path(file).is_file():
                    response = self.fetch("https://"+site+url[1]+"/")
                    if response == False: return False

                    post = re.findall('<div class="message-userContent lbContainer.*? · (.*?)">.*?article.*?>(.*?)<\/article>',response, re.MULTILINE | re.DOTALL)
                    data = {'id':url[2],'date':post[0][0],'user':url[0],'post':post[0][1]}
                    with open(file, 'w') as f:
                        json.dump(data, f)
                else:
                    print(url[2],"already exist")
                    scans = scans +1
                    if scans == 20:
                        return True

            count = count +1

    def vanilla(self,cat,site):
        currentOffers,count,src = "",1,"https://"+site+".com/categories/"+cat+"/p"
        dataDir,scans = os.getcwd()+"/src/"+site+"/"+cat+"/",0

        print("Checking",site)
        response = self.fetch("https://"+site+".com")
        if response == False: return False
        if self.checkCF(response):
            print("Failed to bypass CF")
            return False

        while True:

            print("Getting",cat)
            response = self.fetch(src+str(str(count)+".json"))
            if response == False: return False
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
                    scans = scans +1
                    if scans == 20:
                        return True

            count = count +1

    def getPostsLowendtalk(self,html,site):
        dataDir = os.getcwd()+"/src/"+site+"/posts/"
        if not os.path.exists(dataDir):
            os.makedirs(dataDir)
        print("Parsing posts")
        posts = re.findall('<li class="Item ItemComment (.*?)" id="Comment_([0-9]+)">.*?profile\/(.*?)".*?datetime="(.*?)".*?Item-Body">(.*?)<div class="(Signature|ThankedByBox|Reactions)',html, re.MULTILINE | re.DOTALL)
        for post in posts:
            urls = re.findall('href="(?!https:\/\/www.lowendtalk|\/discussion|class="QuoteFolding).*?"',post[4], re.MULTILINE | re.DOTALL)
            tags = ["Provider","Administrator"]
            if any(tag in post[0] for tag in tags) and urls:
                file = dataDir+post[1]+"-"+post[2]+".json"
                if not Path(file).is_file():
                    data = {'id':post[1],'date':post[3],'user':post[2],'post':post[4]}
                    with open(file, 'w') as f:
                        json.dump(data, f)

    def threads(self):
        threadsPath,page = os.getcwd()+"/src/threads.json",1
        print("Loading "+threadsPath)
        with open(threadsPath, 'r') as f:
            threads = json.load(f)
        for url in threads:
            page = 1
            if "lowendtalk.com" in url:
                while True:
                    html = self.fatch(url+str(page))
                    if self.checkCF(html):
                        print("Failed to bypass CF")
                        return False
                    if "The page you were looking for could not be found." in html:
                        print("End of line")
                        break
                    self.getPostsLowendtalk(html,"lowendtalk")
                    page = page +1
            else:
                print("Not defined")
