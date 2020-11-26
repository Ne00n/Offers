# Offers

![data mining](https://media.tenor.com/images/a8e3545e271bab5d3848c3f15ccb61ef/tenor.gif)

**Dependencies**<br />
```
pip3 install PyVirtualDisplay
pip3 install selenium
pip3 install fake-useragent
pip3 install dnspython  #generate
pip3 install tldextract #generate
pip3 install matplotlib #stats
```

**Updating dataset**<br />
```
python3 run.py update
python3 run.py headless #for servers => apt-get install xvfb
```

**Updating /data**<br />
```
python3 run.py generate
```

**Updating /data + domains.json**<br />
```
python3 run.py dns
```
