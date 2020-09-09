# coding = utf-8
import re
import requests
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import os

def geturls():
    urls = []

    baseurl = 'https://movie.douban.com/chart'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'}
    chart = requests.get(baseurl, headers=headers)
    button_pattern = re.compile(
        'type_name=[\u4e00-\u9fa5]+&type=\d+')
    for result in button_pattern.findall(chart.text):
        urls.append('https://movie.douban.com/typerank?' +
                    result + '&interval_id=100:90&action=')

    driver = webdriver.Chrome(r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")
    url_pattern = re.compile(r'https://movie.douban.com/subject/\d+/')
    urlset = set()
    for i in urls:
        driver.get(i)
        for i in range(3):
            scroll = "window.scrollTo(0, document.body.scrollHeight)"
            driver.execute_script(scroll)
            time.sleep(0.5)
        for result in url_pattern.findall(driver.page_source):
            urlset.add(result)
    file = open('urls.txt', 'w', encoding='utf-8')
    for i in urlset:
        file.writelines(i + '\n')
    file.close()

def recoverurls():
    urls = []
    film_files = os.listdir(os.path.abspath('./filmdata'))
    print(len(film_files))
    for film_file in film_files:
        urls.append('https://movie.douban.com/subject/' + film_file.split('.json')[0] + '/')
    files = open('urls.txt', 'w', encoding='utf-8')
    for i in urls:
        files.writelines(i + '\n')
    files.close()
if __name__ == "__main__":
    # geturls()
    recoverurls()
