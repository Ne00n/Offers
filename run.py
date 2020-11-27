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
    Update.lowendbox()
    Update.close(headless)

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
    Update.getUrls("shared-hosting-offers","lowendtalk")

param = sys.argv
if len(param) == 1:
    print("update generate dns stats")
elif sys.argv[1] == "generate" and len(sys.argv) > 2 and sys.argv[2] == "slow":
    generate(True)
elif sys.argv[1] == "generate":
    generate()
elif sys.argv[1] == "dns":
    Data = Data()
    Data.getUrls("offers","talk.lowendspirit",True)
    Data.getUrls("offers","lowendtalk",True)
    Data.getUrls("shared-hosting-offers","lowendtalk",True)
elif sys.argv[1] == "update":
    update()
elif sys.argv[1] == "headless":
    update(True)
elif sys.argv[1] == "stats":
    Stats = Stats()
