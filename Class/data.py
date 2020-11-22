#!/usr/bin/python3
import time, json, re, os

class Data:
    def __init__(self):
        print("Data")

    def getProviders(self,cat,site):
        dataDir = os.getcwd()+"/data/"+site+"/"+cat+"/"
        files = os.listdir(dataDir)
        providers = []
        for file in files:
            with open(dataDir+file, 'r') as f:
                data = json.load(f)
            if not data['user'] in providers:
                providers.append(data['user'])
        return providers

    def saveProviders(self,site,providers):
        with open(os.getcwd()+"/data/"+site+"/providers.json", 'w') as f:
            json.dump(providers, f)
