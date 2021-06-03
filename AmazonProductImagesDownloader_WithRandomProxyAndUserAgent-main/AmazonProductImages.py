from random import choice
import random
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
import requests
from bs4 import BeautifulSoup as soup
import time
import pandas
import urllib.request

def proxy_generator():
    response = requests.get("https://free-proxy-list.net/")
    soupp = soup(response.content, 'html5lib')
    proxy = {'https': choice(list(map(lambda x:x[0]+':'+x[1], list(zip(map(lambda x:x.text,soupp.findAll('td')[::8]), map(lambda x:x.text, soupp.findAll('td')[1::8]))))))}
    return proxy

software_names = [SoftwareName.CHROME.value]
operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)




colnames = ['Parent_SKU','Parent_ASIN']
filename="all.csv"
data = pandas.read_csv(filename, names=colnames)

sku = data.Parent_SKU.tolist()
urls  = data.Parent_ASIN.tolist()

#filename="check.txt"
#fr=open(filename,"a",encoding='utf-8')

filename="Error_.csv"
fe=open(filename,"a",encoding='utf-8')

filename="Parent_.csv"
f=open(filename,"a",encoding='utf-8')
itemscraped=1
you_have_proxy = False
proxy_used = 0
got_result = False
for url,sk in zip(urls,sku):
    #headers = { 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36'}
    ua =  user_agent_rotator.get_random_user_agent()   
    headers = {'User-Agent': ua}
    ASIN = url
    url = "https://www.amazon.com/dp/" + url
    
    while 1:
        if you_have_proxy==False or got_result==False:
            you_have_proxy=False
            proxy = proxy_generator()
            ua =  user_agent_rotator.get_random_user_agent()
            print(".")
            #print(str(proxy) + " "+ str(ua))
        try:
            page_html = requests.get(url,headers=headers,proxies=proxy,timeout=9)
            you_have_proxy = True
            proxy_used = 0
            break
        except:
            got_result=False
            pass
    #proxy_used+=1            
    page_soup = soup(page_html.text,features="lxml")
    time.sleep(2)
    itemscraped+=1
    img_link_container = page_soup.find("ul",{"class":"a-unordered-list a-nostyle a-button-list a-vertical a-spacing-top-extra-large"})
    try:
        img_link_temp=img_link_container.findAll('img')
    except:
        fe.write(sk + "," +ASIN + "\n")
        print(url)
        got_result=False
        time.sleep(1)
        continue 
    got_result=True       
    img_link = []
    for link in img_link_temp:
        if "40_.jpg" in link["src"]:
            link["src"]=link["src"].replace("40_.jpg","300_.jpg")
            img_link.append(link["src"])
    img_links = img_link[0]
    #print(str(itemscraped)+" "+img_links)
    sk = sk.replace("/","-")
       
    file = sk + ".jpg"
    fullpath = "images/" + file
    urllib.request.urlretrieve(img_links,fullpath)

    file = ASIN +" edited2020" + ".jpg"
    fullpath = "imag/" + file
    urllib.request.urlretrieve(img_links,fullpath)

    print(str(itemscraped) +" "+ASIN + "," + sk + "," + img_links)
    f.write(ASIN + "," + sk + "," + img_links+ "\n")

    time.sleep(1)