#!/usr/bin/python3
import dns.resolver, ipaddress, tldextract, time, pprint, json, html, re, os
from time import sleep

class Data:
    def __init__(self):
        global dnsCache
        dnsCache = {}
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

    def filterUrls(self,url):
        drop = ['twitter.com','facebook.com','imgur.com','github.com','speedtest.net','he.net','google.com','trustpilot.com','arin.net','webhostingtalk.com','discord.gg',
        'youtube.com','tenor.com','instagram.com','githubusercontent.com']
        if any(domain in url for domain in drop):
            return True
        return False

    def resolve(self,domain):
        nameservers,count = [],0
        while count < 3:
            try:
                answers = dns.resolver.query(domain,'NS')
                for server in answers:
                    nameservers.append(server.target.to_text())
                nameservers.sort()
                return nameservers
            except:
                sleep(0.5)
            count += 1
        return False

    def appendDic(self,dict,list,user):
        for entry in list:
            dict[user]['urls'][entry] = list[entry]
        return dict

    def getUrls(self,cat,site,resolve=False):
        dataDir = os.getcwd()+"/src/"+site+"/"+cat+"/"
        files = os.listdir(dataDir)
        data,domains,dead,alive = [],{},[],[]
        for file in files:
            with open(dataDir+file, 'r') as f:
                post = json.load(f)
            urlsRaw = re.findall("(https?:\/\/[A-Za-z0-9.\/?=&;_-]*)",post['post'], re.MULTILINE | re.DOTALL)
            #urls = self.filterUrls(urlsRaw)
            urls = list(set(urlsRaw))
            urls.sort()
            filtered = {}
            for url in urls:
                url = re.sub('&lt;br$', '', url)
                url = re.sub('<[^<]+?>', '', html.unescape(url))
                url = url.replace("_","")
                if resolve:
                    domain = tldextract.extract(url).domain + "." + tldextract.extract(url).suffix
                    if self.filterUrls(domain):
                        continue
                    if domain in filtered:
                        continue
                    if domain in dead:
                        continue
                    if domain in dnsCache:
                        print("Getting NS from Cache for",domain)
                        filtered[domain] = dnsCache[domain]
                        continue
                    try:
                        ipaddress.ip_address(domain[:-1])
                        print("Filtered",domain)
                        continue
                    except:
                        nameservers = []
                        print("Getting NS for",domain)
                        nameservers = self.resolve(domain)
                        if nameservers == False:
                            print("NS not found for",domain)
                            dead.append(domain)
                        else:
                            dnsCache[domain] = nameservers
                            alive.append(domain)
                        sleep(0.10)
                        filtered[domain] = nameservers
            if post['user'] in domains:
                if domains[post['user']]['urls'] == None and filtered != None:
                    domains[post['user']] = {'urls':filtered}
                else:
                    domains = self.appendDic(domains,filtered,post['user'])
            else:
                domains[post['user']] = {'urls':filtered}
            data.append({'id':post['id'],'user':post['user'],'post':{'date':post['date'],'urls':urls}})
        data = sorted(data, key=lambda k: k['id'],  reverse=True)
        with open(os.getcwd()+"/data/"+site+"-urls-"+cat+".json", 'w') as f:
            json.dump(data, f, indent=2)
        if resolve:
            domains = {k: domains[k] for k in sorted(domains)}
            alive.sort()
            dead.sort()
            with open(os.getcwd()+"/data/"+site+"-domains-"+cat+".json", 'w') as f:
                json.dump(domains, f, indent=2)
            with open(os.getcwd()+"/data/"+site+"-domains-dead-"+cat+".json", 'w') as f:
                json.dump(dead, f, indent=2)
            with open(os.getcwd()+"/data/"+site+"-domains-alive-"+cat+".json", 'w') as f:
                json.dump(alive, f, indent=2)
