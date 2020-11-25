#!/usr/bin/python3
import matplotlib.pyplot as plt
from datetime import date
import pprint, json, os, re
import numpy as np

class Stats:
    def __init__(self):
        print("Stats")
        print("Loading deadpool.json")
        with open(os.getcwd()+"/src/deadpool.json", 'r') as f:
            deadpoolJson = json.load(f)
        print("Loading colocrossing.json")
        with open(os.getcwd()+"/src/colocrossing.json", 'r') as f:
            colocrossingJson = json.load(f)

        data = self.get("lowendbox","posts",deadpoolJson,colocrossingJson)
        self.posts(data,'lowendbox')
        self.postsCat(data,'lowendbox')
        data = self.get('lowendtalk','offers',deadpoolJson,colocrossingJson)
        self.posts(data,'lowendtalk',30)
        data = self.get('talk.lowendspirit','offers',deadpoolJson,colocrossingJson)
        self.posts(data,'talk.lowendspirit',30)

    def get(self,site,cat,deadpoolJson,colocrossingJson):
        dataDir = os.getcwd()+"/src/"+site+"/"+cat+"/"
        files = os.listdir(dataDir)



        data =  {}
        data['posts'],data['total'],data['other'],data['deadpool'],data['colocrossing'] = 0,{},{},{},{}
        for file in files:
            with open(dataDir+file, 'r') as f:
                post = json.load(f)

            if site == "lowendbox":
                nameRaw = re.findall(", by (.*?)<\/div>",post['post'], re.MULTILINE | re.DOTALL)
                name = nameRaw[0]
            elif site == "lowendtalk" or "talk.Lowendspirit":
                name = post['user']

            if not name in data['total']:
                data['total'][name] = 0
            if not name in data['other']:
                data['other'][name] = 0
            if not name in data['deadpool']:
                data['deadpool'][name] = 0
            if not name in data['colocrossing']:
                data['colocrossing'][name] = 0

            if any(deadpool in post['post'] for deadpool in deadpoolJson):
                data['deadpool'][name] = data['deadpool'][name] +1
            elif any(colocrossing in post['post'] for colocrossing in colocrossingJson):
                data['colocrossing'][name] = data['colocrossing'][name] +1
            else:
                data['other'][name] = data['other'][name] +1

            data['total'][name] = data['total'][name] +1
            data['posts'] = data['posts'] +1

        data['total'] = {k: v for k, v in sorted(data['total'].items(), key=lambda item: item[1], reverse=True)}
        return data

    def posts(self,data,site,length=14):
        print(site,"Posts")
        today = date.today()

        labels = list(data['total'].keys())[:80]
        posts = list(data['total'].values())[:80]
        width = 0.35

        fig, ax = plt.subplots()

        ax.bar(labels, posts, width, label='Posts')

        ax.set_ylabel('Posts')
        ax.set_title(site+'.com '+str(data['posts'])+' Posts, '+str(today.strftime("%d/%m/%Y")))
        ax.legend()

        plt.xticks(rotation=65)
        fig.tight_layout()

        figure = plt.gcf()
        figure.set_size_inches(length, 8)

        plt.savefig('img/'+site+'Posts.png', dpi=300)

    def postsCat(self,data,site):
        print(site,"Posts Categories")
        today = date.today()

        labels = list(data['other'].keys())
        other = list(data['other'].values())
        deadpool = list(data['deadpool'].values())
        colocrossing = list(data['colocrossing'].values())
        width = 0.35

        fig, ax = plt.subplots()

        ax.bar(labels, other, width, label='Other')
        ax.bar(labels, deadpool, width, bottom=other, label='Deadpool')
        ax.bar(labels, colocrossing, width, label='Colocrossing')

        ax.set_ylabel('Posts')
        ax.set_title('Lowendbox.com '+str(data['posts'])+' Posts, '+str(today.strftime("%d/%m/%Y")))
        ax.legend()

        plt.xticks(rotation=65)
        fig.tight_layout()

        figure = plt.gcf()
        figure.set_size_inches(14, 8)

        plt.savefig('img/'+site+'PostsCategories.png', dpi=300)
