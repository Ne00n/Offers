#!/usr/bin/python3
from Class.base import Base
from Class.data import Data
from Class.stats import Stats
import sys

param = sys.argv
if len(param) == 1:
    print("update generate dns stats")
elif sys.argv[1] == "generate":
    Data = Data()
    offers = Data.getProviders("offers","lowendtalk")
    shared = Data.getProviders("shared-hosting-offers","lowendtalk")
    providers = offers + shared
    providers = list(set(providers))
    Data.saveProviders("lowendtalk",providers)
    list = Data.getProviders("offers","talk.lowendspirit")
    Data.saveProviders("talk.lowendspirit",list)
    Data.getUrls("offers","talk.lowendspirit")
    Data.getUrls("offers","lowendtalk")
    Data.getUrls("shared-hosting-offers","lowendtalk")
elif sys.argv[1] == "dns":
    Data = Data()
    Data.getUrls("offers","talk.lowendspirit",True)
    Data.getUrls("offers","lowendtalk",True)
    Data.getUrls("shared-hosting-offers","lowendtalk",True)
elif sys.argv[1] == "update":
    Base = Base()
    Base.vanilla("offers","lowendtalk")
    Base.vanilla("shared-hosting-offers","lowendtalk")
    Base.vanilla("offers","talk.lowendspirit")
    Base.lowendbox()
    Base.close()
elif sys.argv[1] == "stats":
    Stats = Stats()
