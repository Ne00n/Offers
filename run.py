#!/usr/bin/python3
from Class.base import Base
from Class.data import Data
import sys

param = sys.argv
if len(param) == 1:
    print("update generate")
elif sys.argv[1] == "generate":
    Data = Data()
    offers = Data.getProviders("offers","lowendtalk")
    shared = Data.getProviders("shared-hosting-offers","lowendtalk")
    list = offers + shared
    Data.saveProviders("lowendtalk",list)
    list = Data.getProviders("offers","talk.lowendspirit")
    Data.saveProviders("talk.lowendspirit",list)
    Data.getUrls("offers","talk.lowendspirit")
    Data.getUrls("offers","lowendtalk")
    Data.getUrls("shared-hosting-offers","lowendtalk")
elif sys.argv[1] == "update":
    Base = Base()
    Base.vanilla("offers","lowendtalk")
    Base.vanilla("shared-hosting-offers","lowendtalk")
    Base.vanilla("offers","talk.lowendspirit")
    Base.lowendbox()
    Base.close()
