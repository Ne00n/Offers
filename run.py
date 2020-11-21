#!/usr/bin/python3
from Class.base import Base

Base = Base()
Base.let("offers")
Base.let("shared-hosting-offers")
Base.letProviders()
Base.close()
