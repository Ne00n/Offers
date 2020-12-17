#!/usr/bin/python3
import dns.resolver, ipaddress, tldextract, random, time, pprint, json, html, re, os
from time import sleep

class Data:
    def __init__(self,slowIn):
        global dnsCache,slow
        dnsCache = {}
        slow = slowIn
        print("Generate")

    def getProviders(self,cat,site):
        dataDir = os.getcwd()+"/src/"+site+"/"+cat+"/"
        files = os.listdir(dataDir)
        providers = []
        for file in files:
            if slow:
                sleep(0.02)
            print("Reading",file)
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
        'youtube.com','tenor.com','instagram.com','githubusercontent.com','secure.gravatar.com','linkedin.com','lowendbox.com/wp-content/','lowendbox.com/tag/','goo.gl',
        'cachefly.net','....','...']
        if any(domain in url for domain in drop):
            return True
        return False

    def resolve(self,domain,type="NS",deadDomains=list()):
        nameservers,count = [],1
        print("Getting "+type+" for",domain)
        while count < 3:
            try:
                answers = dns.resolver.query(domain,type)
                for server in answers:
                    if type is "NS":
                        nameservers.append(server.target.to_text())
                    else:
                        nameservers.append(server.to_text())
                nameservers.sort()
                return nameservers
            except:
                if domain in deadDomains or type == "PTR":
                    print("Skipping dead",domain)
                    return False
                wait = round(random.uniform(0.5,4), 2) * count
                print("Waiting",wait,"seconds")
                sleep(wait)
            count += 1
        return False

    def appendDic(self,dict,list,user):
        for entry in list:
            dict[user]['urls'][entry] = list[entry]
        return dict

    def getUrls(self,cat,site,resolve=False):
        dataDir = os.getcwd()+"/src/"+site+"/"+cat+"/"
        files = os.listdir(dataDir)
        deadPath = os.getcwd()+"/data/"+site+"-domains-dead-"+cat+".json"
        if os.path.exists(deadPath):
            print("Loading "+site+"-domains-dead-"+cat+".json")
            with open(deadPath, 'r') as f:
                deadDomains = json.load(f)
        else:
            deadDomains = list()
        data,domains,dead,alive,ip = [],{},[],[],{}
        for file in files:
            if slow:
                sleep(0.02)
            print("Reading",file)
            with open(dataDir+file, 'r') as f:
                post = json.load(f)
            urlsRaw = re.findall("(https?:\/\/[A-Za-z0-9.\/?=&;_-]{1,}\.[A-Za-z0-9.\/?=&;_-]{1,})",post['post'], re.MULTILINE | re.DOTALL)
            ipsRaw = re.findall("[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}",post['post'], re.MULTILINE | re.DOTALL)
            #urls = self.filterUrls(urlsRaw)
            urls = list(set(urlsRaw))
            ips = list(set(ipsRaw))
            urls.sort()
            ips.sort()
            filtered = {}
            for url in urls:
                url = re.sub('&lt;br$', '', url)
                url = re.sub('<[^<]+?>', '', html.unescape(url))
                url = url.replace("_","")
                if resolve:
                    domain = tldextract.extract(url).domain + "." + tldextract.extract(url).suffix
                    domain = domain.lower()
                    if self.filterUrls(domain): continue
                    if domain in filtered: continue
                    if domain in dead: continue
                    if domain in dnsCache:
                        print("Getting NS from Cache for",domain)
                        filtered[domain] = {}
                        filtered[domain]['ns'] = dnsCache[domain]['ns']
                        filtered[domain]['a'] = dnsCache[domain]['a']
                        continue
                    try:
                        ipaddress.ip_address(domain[:-1])
                        print("Filtered",domain)
                        continue
                    except:
                        nameservers,aRecords,targets = [],[],{}
                        nameservers = self.resolve(domain,'NS',deadDomains)
                        if nameservers == False:
                            print("NS not found for",domain)
                            aRecords = False
                            dead.append(domain)
                        else:
                            aRecords = self.resolve(domain,'A')
                            if aRecords is not False:
                                for entry in aRecords:
                                    try:
                                        ipRDNS = dns.reversename.from_address(entry)
                                        rdns = self.resolve(ipRDNS,'PTR')
                                        targets[entry] = rdns
                                    except:
                                        print("Failed to get RDNS from",entry)
                                        targets[entry] = False
                            dnsCache[domain] = {}
                            dnsCache[domain]['ns'] = nameservers
                            if not targets: targets = False
                            dnsCache[domain]['a'] = targets
                            alive.append(domain)
                        sleep(0.10)
                        filtered[domain] = {}
                        filtered[domain]['ns'] = nameservers
                        filtered[domain]['a'] = targets
            if site == "lowendbox":
                dataRaw = re.findall("Date\/Time:.*?> (.*?), by (.*?)<\/div>",post['post'], re.MULTILINE | re.DOTALL)
                post['user'] = dataRaw[0][1]
                post['date'] = dataRaw[0][0]
                post['id'] = int(post['id'])
                for url in list(urls):
                    if self.filterUrls(url):
                        urls.remove(url)
            if post['user'] in domains:
                if domains[post['user']]['urls'] == None and filtered != None:
                    domains[post['user']] = {'urls':filtered}
                else:
                    domains = self.appendDic(domains,filtered,post['user'])
            else:
                domains[post['user']] = {'urls':filtered}
            if post['user'] in ip and ips:
                for entry in ips:
                    ip[post['user']].append(entry)
                    ip[post['user']] = list(set(ip[post['user']]))
                    ip[post['user']].sort()
            elif ips:
                ip[post['user']] = []
                for entry in ips:
                    ip[post['user']].append(entry)
                    ip[post['user']] = list(set(ip[post['user']]))
                    ip[post['user']].sort()
            data.append({'id':post['id'],'user':post['user'],'post':{'date':post['date'],'urls':urls}})
        data = sorted(data, key=lambda k: k['id'],  reverse=True)
        with open(os.getcwd()+"/data/"+site+"-urls-"+cat+".json", 'w') as f:
            json.dump(data, f, indent=2)
        if ip:
            ip = {k: ip[k] for k in sorted(ip)}
            with open(os.getcwd()+"/data/"+site+"-ips-"+cat+".json", 'w') as f:
                json.dump(ip, f, indent=2)
        if resolve:
            domains = {k: domains[k] for k in sorted(domains)}
            for user,data in domains.items():
                data['urls'] = {k: data['urls'][k] for k in sorted(data['urls'])}
            alive.sort()
            dead.sort()
            with open(os.getcwd()+"/data/"+site+"-domains-"+cat+".json", 'w') as f:
                json.dump(domains, f, indent=2)
            with open(os.getcwd()+"/data/"+site+"-domains-dead-"+cat+".json", 'w') as f:
                json.dump(dead, f, indent=2)
            with open(os.getcwd()+"/data/"+site+"-domains-alive-"+cat+".json", 'w') as f:
                json.dump(alive, f, indent=2)

    def webserver(self):
        dataDir = os.getcwd()+"/data/"
        files = os.listdir(dataDir)
        for file in files:
            if "domains" in file and not "dead" in file and not "alive" in file:
                with open(dataDir+file, 'r') as f:
                    domains = json.load(f)
                for key,value in domains.items():
                    for domain,nameservers in value['urls'].items():
                        print(domain)
                        print(nameservers)
                        return False
