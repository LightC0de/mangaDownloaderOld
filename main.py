# coding: utf-8
import requests
import re
import os
from bs4 import BeautifulSoup
from lxml import html

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

def main():
  print('Введите ссылку на мангу:')
  url_manga = input()

  # Парсим с главной странцы манги ссылку на чтение глав
  first_r = requests_r(url_manga)
  url_read = html.fromstring(first_r).xpath('//span[@class = "read-first"]/a/@href')[0] 

  # Парсим список ссылок на главы
  print('Парсим список ссылок на главы.')
  second_r = requests_r('http://readmanga.me' + url_read)
  selectors = html.fromstring(second_r).xpath('//select[@id = "chapterSelectorSelect"]/option/@value')

  # Проверка на "?mtr=1"
  if(selectors):
    pass
  else:
    second_r = requests_r('http://readmanga.me' + url_read + '?mtr=1')
    selectors = html.fromstring(second_r).xpath('//select[@id = "chapterSelectorSelect"]/option/@value')

  selectors.reverse()
  i_img = 0

  for selector in selectors:
    # Парсим ссылки на картинки с одной главы
    imgs_r = requests_r('http://readmanga.me' + selector)
    urls = []
    result = re.findall(r'rm_h\.init\((.+\]\])', imgs_r)[0].split("],")
    for item in result:
      res = re.findall(r'\[\'\',\'(.+)\',"(.+)"', item)
      urls.append(res[0][0] + res[0][1])

    # Сохраняем картинки в папку
    # Создание структуры
    img_folder = selector.split("?")[0].split("/")
    img_folder_manga = img_folder[len(img_folder)-3]
    img_folder_vol = img_folder[len(img_folder)-2]
    img_folder_ch = img_folder[len(img_folder)-1]
    img_link_folder = img_folder_manga + '/' + img_folder_vol + '/' + img_folder_ch + '/'

    try:
      os.makedirs(img_link_folder)
    except OSError:
      pass

    for url in urls:
      img_name = url.split("?")[0].split("/")
      img_name = img_name[len(img_name)-1]
      r = requests.get(url, allow_redirects=True)
      open(img_link_folder + img_name, 'wb').write(r.content)
      print('Сохранено: ' + img_link_folder + img_name)
      i_img += 1;

  print('\nСохранение завершено успешно!')
  print('Скачано: ' + str(i_img) + ' картинок.\n')
  res_next = input('Хотите скачать ещё мангу? [Д/н] ')
  if (res_next == 'y' or res_next == 'yes' or res_next == 'д' or res_next == 'да'):
    main()
  else:
    input('Чтобы закрыть программу нажмите ENTER .')

print('Скрипт mangaDownloader | https://github.com/LightC0de/mangaDownloader')
main()