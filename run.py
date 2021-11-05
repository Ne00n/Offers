#!/usr/bin/python3
from Class.base import Base
from Class.data import Data
from Class.stats import Stats
import sys

def update(headless=False):
    Update = Base(headless)
    Update.vanilla("offers","lowendtalk")
    Update.vanilla("shared-hosting-offers","lowendtalk")
    Update.vanilla("offers","talk.lowendspirit")
    Update.discourse("offers","hostedtalk.net")
    Update.xenforo("vps-cloud-offers.10","vpsboard.com")
    Update.xenforo("vps-hosting-offers.204","hostingdiscussion.com")
    #Update.xenforo("shared-hosting-offers.203","hostingdiscussion.com")
    #Update.xenforo("dedicated-hosting-offers.200","hostingdiscussion.com")
    #Update.vBulletin("forumdisplay.php?f=104","www.webhostingtalk.com")
    Update.lowendbox()
    Update.close()

def generate(slow=False):
    Update = Data(slow)
    offers = Update.getProviders("offers","lowendtalk")
    shared = Update.getProviders("shared-hosting-offers","lowendtalk")
    providers = offers + shared
    providers = list(set(providers))
    Update.saveProviders("lowendtalk",providers)
    providers = Update.getProviders("offers","talk.lowendspirit")
    Update.saveProviders("talk.lowendspirit",providers)
    Update.getUrls("offers","talk.lowendspirit")
    Update.getUrls("offers","lowendtalk")
    Update.getUrls("posts","lowendtalk")
    Update.getUrls("shared-hosting-offers","lowendtalk")
    Update.getUrls("posts","lowendbox")
    Update.getUrls("offers","hostedtalk.net")
    Update.getUrls("vps-cloud-offers.10","vpsboard.com")
    Update.getUrls("vps-hosting-offers.204","hostingdiscussion.com")

def threads(headless=False):
    Update = Base(headless)
    Update.threads()
    Update.close()

param = sys.argv
if len(param) == 1:
    print("update generate dns stats")
elif sys.argv[1] == "generate" and len(sys.argv) > 2 and sys.argv[2] == "slow":
    generate(True)
elif sys.argv[1] == "generate":
    generate()
elif sys.argv[1] == "dns":
    Data = Data(False)
    Data.getUrls("offers","talk.lowendspirit",True)
    Data.getUrls("offers","lowendtalk",True)
    Data.getUrls("posts","lowendtalk",True)
    Data.getUrls("shared-hosting-offers","lowendtalk",True)
    Data.getUrls("posts","lowendbox",True)
    Data.getUrls("offers","hostedtalk.net",True)
    Data.getUrls("vps-cloud-offers.10","vpsboard.com",True)
    Data.getUrls("vps-hosting-offers.204","hostingdiscussion.com",True)
elif sys.argv[1] == "update":
    update()
elif sys.argv[1] == "headless":
    update(True)
elif sys.argv[1] == "stats":
    Stats = Stats()
elif sys.argv[1] == "webserver":
    Data = Data(False)
    Data.webserver()
elif sys.argv[1] == "threads" and len(sys.argv) > 2 and sys.argv[2] == "headless":
    threads(True)
elif sys.argv[1] == "threads":
    threads()
