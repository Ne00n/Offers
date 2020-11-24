#!/usr/bin/python3
import matplotlib.pyplot as plt
from datetime import date
import pprint, json, os, re
import numpy as np

class Stats:
    def __init__(self):
        print("Stats")
        data = self.getLEB()
        self.postsLEB(data)
        self.postsLEBCat(data)

    def getLEB(self):
        dataDir = os.getcwd()+"/src/lowendbox/posts/"
        files = os.listdir(dataDir)

        print("Loading deadpool.json")
        with open(os.getcwd()+"/src/deadpool.json", 'r') as f:
            deadpoolJson = json.load(f)
        print("Loading colocrossing.json")
        with open(os.getcwd()+"/src/colocrossing.json", 'r') as f:
            colocrossingJson = json.load(f)

        data =  {}
        data['posts'],data['total'],data['other'],data['deadpool'],data['colocrossing'] = 0,{},{},{},{}
        for file in files:
            with open(dataDir+file, 'r') as f:
                post = json.load(f)

            nameRaw = re.findall(", by (.*?)<\/div>",post['post'], re.MULTILINE | re.DOTALL)

            if not nameRaw[0] in data['total']:
                data['total'][nameRaw[0]] = 0
            if not nameRaw[0] in data['other']:
                data['other'][nameRaw[0]] = 0
            if not nameRaw[0] in data['deadpool']:
                data['deadpool'][nameRaw[0]] = 0
            if not nameRaw[0] in data['colocrossing']:
                data['colocrossing'][nameRaw[0]] = 0

            if any(deadpool in post['post'] for deadpool in deadpoolJson):
                data['deadpool'][nameRaw[0]] = data['deadpool'][nameRaw[0]] +1
            elif any(colocrossing in post['post'] for colocrossing in colocrossingJson):
                data['colocrossing'][nameRaw[0]] = data['colocrossing'][nameRaw[0]] +1
            else:
                data['other'][nameRaw[0]] = data['other'][nameRaw[0]] +1

            data['total'][nameRaw[0]] = data['total'][nameRaw[0]] +1
            data['posts'] = data['posts'] +1

        data['total'] = {k: v for k, v in sorted(data['total'].items(), key=lambda item: item[1], reverse=True)}
        return data

    def postsLEB(self,data):
        print("Lowendbox Posts")
        today = date.today()

        labels = list(data['total'].keys())
        posts = list(data['total'].values())
        width = 0.35

        fig, ax = plt.subplots()

        ax.bar(labels, posts, width, label='Posts')

        ax.set_ylabel('Posts')
        ax.set_title('Lowendbox.com '+str(data['posts'])+' Posts, '+str(today.strftime("%d/%m/%Y")))
        ax.legend()

        plt.xticks(rotation=65)
        fig.tight_layout()

        figure = plt.gcf()
        figure.set_size_inches(14, 8)

        plt.savefig('img/lowendboxPosts.png', dpi=300)

    def postsLEBCat(self,data):
        print("Lowendbox Posts Categories")
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

        plt.savefig('img/lowendboxPostsCategories.png', dpi=300)
