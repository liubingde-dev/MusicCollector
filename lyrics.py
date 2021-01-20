# coding=utf-8

import os

import requests
from bs4 import BeautifulSoup


def crawl(num):
    url = "http://www.9ku.com/play/" + str(num) + ".htm"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    soup = BeautifulSoup(response.text, 'lxml')
    lyrics = soup.find_all(id="lrc_content")
    return lyrics


def get_music_lyrics(start_page, end_page, step):
    file_path_base = "D:\music\lyrics\\"
    for page in range(start_page, end_page):
        begin = page * step + 1
        list = []
        for index in range(begin, begin + step):
            result_list = crawl(index)
            if result_list != None and len(result_list) > 0:
                list.append(result_list[0].string)
                sub_path = file_path_base + str(page) + "\\"
                if not os.path.exists(sub_path):
                    os.mkdir(sub_path)
                file_name = sub_path + str(index) + ".txt"
                print(file_name)
                if result_list[0].string != None:
                    with open(file_name, 'w', encoding='utf-8') as f:
                        f.write(result_list[0].string)
                        f.flush()


if __name__ == '__main__':
    get_music_lyrics(50, 55, 1000)
