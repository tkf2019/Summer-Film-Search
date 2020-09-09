# coding = utf-8
import encodings
from attr import attrs
from bs4 import BeautifulSoup
import re
import urllib.error
from numpy.distutils.misc_util import is_string
from numpy.ma.core import append
from pandas import json_normalize
import requests
import time
import json
import os
import tqdm
import codecs

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
    'Cookies': 'bid=i71qWLhps-I; __yadk_uid=439uO6Ii3FHILrdFwM8T8Zaq887ZGIhb; douban-fav-remind=1; __gads=ID=e6245c619a94a8b2:T=1594644098:S=ALNI_MZCu6-Fqnk3gaVdUJzDjPu5bkvG_w; gr_user_id=7b206869-fc24-4acc-bc4f-2a097d054898; _vwo_uuid_v2=DE7AFD340E6206D9CD1893028BAF3130D|fffc374a4bf293b0dfb2b09f6906b00c; viewed="26723433_11442895_4238362_2969029_30401373_6388661_26382433_26425831_26306686"; ll="108288"; push_doumail_num=0; push_noty_num=0; __utmv=30149280.20103; __utmc=30149280; __utmc=223695111; __utma=30149280.325173359.1594204180.1599469899.1599471770.17; __utmz=30149280.1599471770.17.8.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmt=1; __utmb=30149280.5.10.1599471770; dbcl2="201033917:Deb5dm4uU/c"; ck=MYl2; __utma=223695111.1625511147.1594204180.1599469899.1599471793.15; __utmb=223695111.0.10.1599471793; __utmz=223695111.1599471793.15.6.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/passport/login; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1599471793%2C%22https%3A%2F%2Faccounts.douban.com%2Fpassport%2Flogin%3Fredir%3Dhttps%253A%252F%252Fmovie.douban.com%252F%22%5D; _pk_ses.100001.4cf6=*; _pk_id.100001.4cf6=7bf343c63666158a.1594204180.14.1599471801.1599469908.'
}

def main():
    film_files = os.listdir(os.path.abspath('../filmdata'))
    celebrities = set()
    for json_file in film_files:
        with codecs.open(os.path.abspath('../filmdata') + '/' + json_file, 'r', encoding='utf-8', errors='ignore') as fp:
            json_result = json.load(fp)
        for actor in json_result['actor']:
            celebrities.add('https://movie.douban.com' + actor)
    
    clist = []
    for item in celebrities:
        clist.append(item)
    l = tqdm.tqdm(clist)
    for url in l:
        id_ = re.compile(
            r'https://movie.douban.com/celebrity/(\d+)/').findall(url)[0]
        l.set_description(id_)
        
        if os.path.exists(id_ + '.json'):
            print('exists')
            continue
        
        time.sleep(1)
        content = requests.get(url.strip(), headers=headers)
        soup = BeautifulSoup(content.text, 'lxml')
        if len(soup.find_all(name='div', attrs={'class': 'info'})) == 0:
            print('failed')
            continue
        
        info_group = {}
        info_group['id'] = re.compile(r'https://movie.douban.com/celebrity/(\d+)/').findall(url)[0]
        info_group['name'] = soup.h1.text
        info_group['image'] = soup.find_all(name='a', attrs={'class': 'nbg'})[0]['href']
        
        intro = soup.find_all(name='div', id='intro')
        if len(intro) != 0:
            info_group['description'] = []
            real = ''
            description = intro[0].find_all(name='span', attrs={'class': 'short'})
            if len(description) == 0:
                real = str(intro[0].find_all(name='div', attrs={'class': 'bd'})[0].text)
            else:
                real = str(intro[0].find_all(name='span', attrs={'class': 'all hidden'})[0].text)
            if real != '':
                for para in real.strip().split('\u3000\u3000'):
                    info_group['description'].append(para.strip())

        info = soup.find_all(name='div', attrs={'class': 'info'})
        if len(info) != 0:
            info_list = info[0].find_all(name='li')
            info_group['gender'] = ''
            info_group['birth-death'] = ''
            info_group['place'] = ''
            info_group['occupation'] = ''

            for li in info_list:
                info_type = li.span.text
                if info_type == '性别':
                    info_group['gender'] = li.text.split('性别:')[1].strip()
                elif info_type == '出生日期':
                    info_group['birth-death'] = li.text.split('出生日期:')[1].strip()
                elif info_type == '生卒日期':
                    info_group['birth-death'] = li.text.split('生卒日期:')[1].strip()
                elif info_type == '出生地':
                    info_group['place'] = li.text.split('出生地:')[1].strip()
                elif info_type == '职业':
                    info_group['occupation'] = li.text.split('职业:')[1].strip()

        with open(info_group['id'] + '.json', 'w', encoding='utf-8') as f:
            json.dump(info_group, f, indent=2, sort_keys=False, ensure_ascii=False)

if __name__ == "__main__":
    main()
