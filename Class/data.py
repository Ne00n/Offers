#!/usr/bin/python3
import time, pprint, json, re, os

class Data:
    def __init__(self):
        print("Generate")

    def getProviders(self,cat,site):
        dataDir = os.getcwd()+"/src/"+site+"/"+cat+"/"
        files = os.listdir(dataDir)
        providers = []
        for file in files:
            with open(dataDir+file, 'r') as f:
                data = json.load(f)
            if not data['user'] in providers:
                providers.append(data['user'])
        return providers

    def saveProviders(self,site,providers):
        providers.sort()
        with open(os.getcwd()+"/data/"+site+"-providers.json", 'w') as f:
            json.dump(providers, f, indent=2)

    def filterUrls(self,urls):
        return urls

    def getUrls(self,cat,site):
        dataDir = os.getcwd()+"/src/"+site+"/"+cat+"/"
        files = os.listdir(dataDir)
        data = []
        for file in files:
            with open(dataDir+file, 'r') as f:
                post = json.load(f)
            urlsRaw = re.findall("(https?:\/\/[A-Za-z0-9.\/?=&;_-]*)",post['post'], re.MULTILINE | re.DOTALL)
            urls = self.filterUrls(urlsRaw)
            urls = list(set(urls))
            data.append({'id':post['id'],'user':post['user'],'post':{'date':post['date'],'urls':urls}})
        data = sorted(data, key=lambda k: k['id'],  reverse=True)
        with open(os.getcwd()+"/data/"+site+"-urls-"+cat+".json", 'w') as f:
            json.dump(data, f, indent=2)
