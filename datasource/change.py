# coding = utf-8
import encodings
from bs4 import BeautifulSoup
import re
import urllib.error
from numpy.distutils.misc_util import is_string
from numpy.ma.core import append
import requests
import os
import time
import json
import codecs

def fix_file():
    actor_files = os.listdir(os.path.abspath('./stardata'))
    for actor_file in actor_files:
        c = ''
        with codecs.open(os.path.abspath('./stardata') + '/' + actor_file, 'r+', encoding='utf-8') as fp:
            f = fp.read()
            c = f.split('}')[1] + '}'
        with codecs.open(os.path.abspath('./stardata') + '/' + actor_file, 'w', encoding='utf-8') as fp:
            fp.write(c)

def build_map():
    film_files = os.listdir(os.path.abspath('./filmdata'))
    for film_file in film_files:
        film_id = re.compile(r'(\d+).json').findall(film_file)[0]
        with codecs.open(os.path.abspath('./filmdata') + '/' + film_file, 'r', encoding='utf-8') as fp:
            film_json = json.load(fp)
        for actor in film_json['actor']:
            actor_id = re.compile(r'/celebrity/(\d+)/').findall(actor)[0]
            if os.path.exists(('./stardata') + '/' + actor_id + '.json'):
                afp = open(os.path.abspath('./stardata') + '/' + actor_id + '.json', 'r+', encoding='utf-8')
                try:
                    actor_json = json.load(afp)
                    actor_json['movies'].append(film_id)
                    afp.truncate()
                    afp.close()
                    wfp = open(os.path.abspath('./stardata') + '/' + actor_id + '.json', 'w', encoding='utf-8') 
                    json.dump(actor_json, wfp, indent=2, sort_keys=False, ensure_ascii=False)
                    wfp.close()
                except ValueError:
                    continue

def find_co():
    actor_files = os.listdir(os.path.abspath('./stardata'))
    for actor_file in actor_files:
        print(actor_file)
        actor_id = re.compile(r'(\d+).json').findall(actor_file)[0]
        fp = open(os.path.abspath('./stardata') + '/' + actor_file, 'r+', encoding='utf-8')
        try:
            actor_json = json.load(fp)
        except  ValueError:
            continue
        fp.truncate()
        fp.close()

        cooperators = {}
        actor_json['cooperators'] = {}
        for movie in actor_json['movies']:
            ffp = open(os.path.abspath('./filmdata') + '/' + movie + '.json', 'r', encoding='utf-8')
            try:
                film_json = json.load(ffp)
                for co in film_json['actor']:
                    co_id = re.compile(r'/celebrity/(\d+)/').findall(co)[0]
                    if co_id != actor_id:
                        if co_id in cooperators:
                            cooperators[co_id] += 1
                        else:
                            cooperators[co_id] = 1
            except ValueError:
                continue
        l = sorted(cooperators.items(), key=lambda x: x[1], reverse=True)
        for key, value in l:
            actor_json['cooperators'][key] = value
        wfp = open(os.path.abspath('./stardata') + '/' + actor_file, 'w', encoding='utf-8')
        json.dump(actor_json, wfp, indent=2, sort_keys=False, ensure_ascii=False)
        wfp.close()

if __name__ == "__main__":
    find_co()
