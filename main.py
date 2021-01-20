# coding=utf-8
import json

import requests
from bs4 import BeautifulSoup
import threading

import sys
import io

#sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
class music(object):
    def __init__(self, author, name, num, url):
        self.name = name
        self.author = author
        self.num = num
        self.url = url


class myThread(threading.Thread):
    def __init__(self,num, begin, end, step):
        threading.Thread.__init__(self)
        self.num=num
        self.begin = begin
        self.end = end
        self.step = step

    def run(self):
        get_music_inf(self.begin, self.end, self.step)
        print("thread"+str(self.num)+"end")


def get_title(tag):
    if "og:title" == tag.get("property"):
        return True
    else:
        return False


def get_artist(tag):
    if "og:music:artist" == tag.get("property"):
        return True
    else:
        return False


def crawl(num):
    url = "http://www.9ku.com/play/" + str(num) + ".htm"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    soup = BeautifulSoup(response.text, 'lxml')
    music_name = soup.head.find_all(get_title)[0].get("content")
    author = soup.head.find_all(get_artist)[0].get("content")
    music_object = music(author, music_name, num, make_sure_url(num))
    print(num)
    return music_object


def make_sure_url(num):
    partition_num = num // 1000 + 1
    url = "http://mp3.9ku.com/mp3/" + str(partition_num) + "/" + str(num) + ".mp3"
    response = requests.get(url)
    if response.status_code == 200:
        return url
    else:
        url = "http://mp3.9ku.com/hot/2004/07-13/" + str(num) + ".mp3"
        response = requests.get(url)
        if response.status_code == 200:
            return url
    return ""


def get_music_inf(page_begin, page_end, step):
    file_path_base = "D:\music\info\\"
    for page in range(page_begin, page_end):
        begin = page * step + 1
        list = []
        for index in range(begin, begin + step):
            music_object = crawl(index)
            if music_object != None:
                list.append(music_object.__dict__)
            file_name = file_path_base + "music_info_" + str(page) + ".json"
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(json.dumps(list, ensure_ascii=False))
            f.flush()


if __name__ == '__main__':
    for index in [26,27,31,41,46,47,48]:
        thread = myThread(index,index, index + 1, 1000)
        thread.start()
        #thread.join()
        print("thread" + str(index))
# get_music_inf(15, 20, 1000)
