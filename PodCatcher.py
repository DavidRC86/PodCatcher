# -*- coding: utf-8 -*-


import requests
from requests import get
from bs4 import BeautifulSoup
import re
from tqdm import tqdm
import tkinter
import time
import math
url = 'https://www.podbean.com/podcast-detail/zy62a-706cb/Disaster-Squad-Podcast'

page = requests.get(url)

page = BeautifulSoup(page.text,'html.parser')

links = [a['href'] for a in page.find_all('a',href = True, class_ = 'download')]

url = links[0]

page = requests.get(url)

page = BeautifulSoup(page.text,'html.parser')



first_link= [a['href'] for a in page.find_all('a',href=re.compile('.mp3'))]

file_names=[]

for name in page.findAll('p',"pod-name"):
    cleanup = name.text[1::].rstrip()
    file_names.append(cleanup)
    
for names in page.findAll('a',"name"):
    file_names.append(names.text)

first_link = str(first_link).replace('[',"").replace(']',"")

dl_links = [a['href'] for a in page.find_all('a',href =re.compile('http.*\.m4a'))]
dl_links.insert(0,first_link)


class DownloadProgressBar(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)

def download(url, file_name):
    r = requests.get(url, stream=True)

    total_size = int(r.headers.get('content-length', 0)); 
    block_size = 1024
    wrote = 0
    
    with open(file_name, "wb") as file:
        for  data in tqdm(r.iter_content(block_size), total=math.ceil(total_size//block_size),unit = 'KB',
                           desc=file_name,leave=True):

            wrote =  wrote + len(data)
            file.write(data)
        return

for i in range(len(file_names)):
    if dl_links[i][-5::] == '.mp3':
        
        download(dl_links[i].replace("'",""),file_names[i]+'.mp3')
    else:
        download(dl_links[i].replace("'",""),file_names[i]+'.m4a')



