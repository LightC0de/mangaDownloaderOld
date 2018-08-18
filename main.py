# coding: utf-8
import requests
import re
from bs4 import BeautifulSoup
from lxml import html

url_manga = 'http://readmanga.me/one_piece__A1b8a09'
headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en,ru;q=0.9,en-US;q=0.8,uk;q=0.7',
        'Connection': 'keep-alive',
        'Host': 'readmanga.me',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
      } 
def requests_r(url):
  return requests.session().get(url, headers = headers).text

# Парсим с главной странцы манги ссылку на чтение глав
first_r = requests_r(url_manga)
url_read = html.fromstring(first_r).xpath('//span[@class = "read-first"]/a/@href')[0] 

# Парсим список ссылок на главы
second_r = requests_r('http://readmanga.me' + url_read)
selectors = html.fromstring(second_r).xpath('//select[@id = "chapterSelectorSelect"]/option/@value')
selectors.reverse()

# Парсим ссылки на картинки с одной главы
imgs_r = requests_r('http://readmanga.me' + selectors[0])
urls = []
result = re.findall(r'rm_h\.init\((.+\]\])', imgs_r)[0].split("],")
for item in result:
  res = re.findall(r'\[\'\',\'(.+)\',"(.+)"', item)
  urls.append(res[0][0] + res[0][1])

# Сохраняем картинки в папку тест
for url in urls:
  img_name = url.split("?")[0].split("/")
  img_name = img_name[len(img_name)-1]
  r = requests.get(url, allow_redirects=True)
  open('test/'+img_name, 'wb').write(r.content)
