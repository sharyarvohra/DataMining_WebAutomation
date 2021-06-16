import urllib
import os
import requests
import urllib.request
import shutil
import re
from slugify import slugify
import time


# Use csv file with the link of images
with open('images.csv', 'r', encoding="utf-8-sig") as csv_file:
    lines = csv_file.readlines()
urls = []
names = []
for line in lines:
    data = line.split(',', 1)
    urls.append(data[0])
    names.append(data[1].replace("=", ""))


def get_photos(url):
    with requests.Session() as c:
        try:
            c.get(url)
            c.headers.update({'referer': url})
            res = c.get(url)
            if res.status_code == 200:
            	return res.content

        except:
            print("On Sleep.!")
            time.sleep(10)
            return get_photos(url)


def get_valid_filename(s):
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)


for url, name in zip(urls, names):
    # print(url)
    download_path = os.path.dirname(os.path.realpath(__file__))
    # print(download_path)
    img_name = name.replace(".", "").replace("-", "_")+"_.png"

    fullpath = str(os.path.dirname(os.path.realpath(__file__))) + \
        "\\"+get_valid_filename(img_name)
    print("Name :"+get_valid_filename(img_name))

    if os.path.exists(fullpath) == True:
        print("Already.!")
        continue

    with open(fullpath, 'wb') as f:
        f.write(get_photos(url))
