# coding = utf-8
import encodings
from bs4 import BeautifulSoup
import re
import urllib.error
from numpy.distutils.misc_util import is_string
from numpy.ma.core import append
import requests
import time
import json
import tqdm
import os

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
    'Cookie': 'bid=i71qWLhps-I; __yadk_uid=439uO6Ii3FHILrdFwM8T8Zaq887ZGIhb; douban-fav-remind=1; __gads=ID=e6245c619a94a8b2:T=1594644098:S=ALNI_MZCu6-Fqnk3gaVdUJzDjPu5bkvG_w; gr_user_id=7b206869-fc24-4acc-bc4f-2a097d054898; _vwo_uuid_v2=DE7AFD340E6206D9CD1893028BAF3130D|fffc374a4bf293b0dfb2b09f6906b00c; viewed="26723433_11442895_4238362_2969029_30401373_6388661_26382433_26425831_26306686"; ll="108288"; __utmz=30149280.1599382093.6.6.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmz=223695111.1599391812.5.4.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; push_noty_num=0; push_doumail_num=0; __utmv=30149280.20103; __utma=30149280.325173359.1594204180.1599436159.1599442186.13; __utma=223695111.1625511147.1594204180.1599436159.1599442186.11; __utmb=223695111.0.10.1599442186; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1599442186%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_ses.100001.4cf6=*; ap_v=0,6.0; __utmc=30149280; __utmb=30149280.9.10.1599442186; __utmc=223695111; _pk_id.100001.4cf6=7bf343c63666158a.1594204180.10.1599446504.1599437570.'
}


def main():
    file = open('urls.txt', 'r', encoding='utf-8')
    flist = []
    for i in file.readlines():
        flist.append(i)
    l = tqdm.tqdm(flist)
    for url in l:
        id_ = re.compile(
            r'https://movie.douban.com/subject/(\d+)/').findall(url)[0]
        l.set_description(id_)

        if os.path.exists(id_ + '.json'):
            print('exist')
            continue
        time.sleep(1)
        content = requests.get(url.strip(), headers=headers)
        soup = BeautifulSoup(content.text, 'lxml')
        if len(soup.find_all('div', id='info')) == 0:
            print('failed')
            continue
        info_list = str(soup.find_all('div', id='info')[0])
        info_group = {}

        info_group['id'] = re.compile(
            r'https://movie.douban.com/subject/(\d+)/').findall(url)[0]

        info_group['name'] = str(soup.title.text).split('(豆瓣)')[0].strip()

        info_group['score'] = str(soup.find_all('strong',  attrs={'property': 'v:average'})[0].text)

        img_pattern = re.compile(r'<img alt=".*?" rel="(.*?)" title="点击看更多海报"/>')
        img_soup = BeautifulSoup(
            str(soup.find_all(name='div', attrs={'id': 'mainpic'})[0]), 'lxml')
        info_group['image'] = img_soup.img.attrs['src']

        info_group['director'] = []
        director_pattern = re.compile(
            r'<a href="/celebrity/\d+/" rel="v:directedBy">(.*?)</a>')
        for director in director_pattern.findall(info_list):
            info_group['director'].append(director)

        info_group['author'] = []
        author_pattern = re.compile(r'<a href="/celebrity/\d+/">(.*?)</a>')
        for author in author_pattern.findall(info_list):
            info_group['author'].append(author)

        info_group['actor'] = []
        star_pattern = re.compile(
            r'<a href="/celebrity/(\d+)/" rel="v:starring">.*?</a>')
        for star in star_pattern.findall(info_list):
            if (len(info_group['actor']) >= 10):
                break
            info_group['actor'].append(star)
        if len(info_group['actor']) == 0:
            continue

        info_group['genre'] = []
        genre_pattern = re.compile(r'<span property="v:genre">(.*?)</span>')
        for genre in genre_pattern.findall(info_list):
            info_group['genre'].append(genre)

        info_group['location'] = []
        location_pattern = re.compile(
            r'<span class="pl">制片国家/地区:</span>(.*?)<br/>')
        for location in location_pattern.findall(info_list):
            info_group['location'].append(location.strip())

        language_pattern = re.compile(
            r'<span class="pl">语言:</span>(.*?)<br/>')
        if len(language_pattern.findall(info_list)) != 0:
            info_group['language'] = language_pattern.findall(info_list)[0].strip()

        date_pattern = re.compile(
            r'property="v:initialReleaseDate">(.*?)</span>')
        if len(date_pattern.findall(info_list)) != 0:
            info_group['date'] = date_pattern.findall(info_list)[0].strip()

        time_pattern = re.compile(
            r'property="v:runtime">(.*?)</span>')
        if len(time_pattern.findall(info_list)) != 0:
            info_group['time'] = time_pattern.findall(info_list)[0].strip()

        if len(soup.find_all(
            name='span', attrs={'property': 'v:summary'})) != 0:
            discription = soup.find_all(
                name='span', attrs={'property': 'v:summary'})[0].text
            all_text = soup.find_all(name='span', attrs={'class': 'all hidden'})
            if len(all_text):
                discription = all_text[0].text
            info_group['description'] = []
            for para in discription.strip().split('\n'):
                if para.strip() != '':
                    info_group['description'].append(para.strip())

        info_group['comment'] = []

        comment_div = soup.find_all(name='div', attrs={'id': 'hot-comments'})
        comment_item = comment_div[0].find_all(name='div', attrs={'class': 'comment'})
        for item in comment_item:
            text = item.find_all(name='span', attrs={'class': 'short'})[0].text
            if len(item.find_all(name='span', attrs={'class': 'hide-item full'})) == 1:
                text = item.find_all(name='span', attrs={'class': 'hide-item full'})[0].text
            info_group['comment'].append(text.strip())
            

        with open(info_group['id'] + '.json', 'w', encoding='utf-8') as f:
            json.dump(info_group, f, indent=2, sort_keys=False, ensure_ascii=False)
    file.close()

if __name__ == "__main__":
    main()
