import requests
from bs4 import BeautifulSoup as soup
import time


with open('link.csv','r') as csv_file:
    lines = csv_file.readlines()
urls = []
for line in lines:
    data = line.split(',')
    urls.append(data[0])

Filename_Details = "Observation_Details.csv"
fd = open(Filename_Details, "a",encoding='utf-8-sig')

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'}  

for url in urls:

    page_html = requests.get(url.replace(" ","").replace("\n",""),headers=headers)
    print("Status Code : "+ str(page_html.status_code))
    page_soup = soup(page_html.content,features="lxml")
    

    category = url.split("detail/")[1]
    category = category.split("/")[0]
    category = category.replace("-"," ")
    category = category.title()
    
    title = page_soup.find("div",{"class":"headProduct"}).h1.get_text() #title
    p_w = page_soup.find("div",{"class":"detail_product_info"}).h4.get_text() #price and weight
    price = p_w.split("per")[0]
    weight = "per"+p_w.split("per")[1]
    try:
        detail = page_soup.find("div",{"class":"detail_product_info"}).findAll("p")[1].span.get_text()
    except :
        detail = page_soup.find("div",{"class":"detail_product_info"}).find("p").get_text()    
    img = page_soup.find("img",{"class":"d-block detail-img"})["src"]

    print(url.replace("," , "-").replace("\n" , " ").replace("\r\n", "").replace("\t", "").replace("\r", ""))
    print(title.replace("," , "-").replace("\n" , " ").replace("\r\n", "").replace("\t", "").replace("\r", ""))


    fd.write(url.replace("," , "-").replace("\n" , " ").replace("\r\n", "").replace("\t", "").replace("\r", ""))
    fd.write(",")
    fd.write(title.replace("," , "-").replace("\n" , " ").replace("\r\n", "").replace("\t", "").replace("\r", ""))
    fd.write(",")
    fd.write(img.replace("," , "-").replace("\n" , " ").replace("\r\n", "").replace("\t", "").replace("\r", ""))
    fd.write(",")
    fd.write(detail.replace("," , "-").replace("\n" , " ").replace("\r\n", "").replace("\t", "").replace("\r", ""))
    fd.write(",")
    fd.write(price.replace("," , "-").replace("\n" , " ").replace("\r\n", "").replace("\t", "").replace("\r", ""))
    fd.write(",")
    fd.write(weight.replace("," , "-").replace("\n" , " ").replace("\r\n", "").replace("\t", "").replace("\r", ""))
    fd.write(",")
    fd.write(category.replace("," , "-").replace("\n" , " ").replace("\r\n", "").replace("\t", "").replace("\r", ""))
    fd.write(",\n")

