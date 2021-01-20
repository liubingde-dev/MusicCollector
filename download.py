# coding=utf-8
import json
import os

import requests
import threading

class myThread(threading.Thread):
    def __init__(self,num):
        threading.Thread.__init__(self)
        self.num=num

    def run(self):
        download(self.num)
        print("thread"+str(self.num)+"end")

def download(num):
    info_path_base = "D:\music\info\\"
    file_path_base = "D:\music\download\\"
    with open(info_path_base + "music_info_" + str(num) + ".json", 'r') as file:
        data = json.load(file)
        print(data)
        for item in data:
            print(item["url"])
            response = requests.get(url=item["url"])
            sub_path = file_path_base + str(num) + "\\"
            if not os.path.exists(sub_path):
                os.mkdir(sub_path)
            file_path = sub_path + str(item["num"]) + ".mp3"
            with open(file_path, "wb") as f:
                f.write(response.content)
                f.flush()


if __name__ == '__main__':
    for index in range(25, 50):
        thread = myThread(index)
        thread.start()
        # thread.join()
        print("thread" + str(index)+"start")

