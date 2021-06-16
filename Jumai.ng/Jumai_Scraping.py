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
    print(url)
    page_html = requests.get(url.replace(" ","").replace("\n",""),headers=headers)
    print("Status Code : "+ str(page_html.status_code))
    page_soup = soup(page_html.content,features="lxml")
    
    try:
        title = page_soup.find("div",{"class":"-fs0 -pls -prl"}).get_text()
    except:
        fd.write("\n")   
        continue 
    try:
        brand = page_soup.find("div",{"class":"-fs14 -pvxs"}).a.get_text()
    except:
        brand = "-"
    img = page_soup.find("div",{"class":"-ptxs -pbs"}).a["href"].replace("680x680","500x500")

    price = page_soup.find("div",{"class":"-hr -pvs -mtxs"}).span.get_text()

    try:
        discount = page_soup.find("div",{"class":"-df -i-ctr"}).span.get_text()
        discount_perc = page_soup.find("span",{"class":"tag _dsct _dyn -mls"}).get_text()
    except:
        discount = "-"  
        discount_perc = "0%"

    prod_details = page_soup.find("div",{"class":"markup -mhm -pvl -oxa"}).get_text()


    spec = page_soup.find("ul",{"class":"-pvs -mvxs -phm -lsn"}).findAll("li")
    Weight = ""
    for i in spec:
        tem = i.get_text()
        if "Weight" in tem:
            Weight = tem.replace("Weight","")

    print(title)
    print(brand)
    print(img)        
    print(price)
    print(discount)
    print(discount_perc)
    print("prod_details : In file directly")
    print(Weight)
    print(prod_details)
    fd.write(url.replace("," , " ").replace("\n" , " "))
    fd.write(",")
    fd.write(title.replace("," , " ").replace("\n" , " "))
    fd.write(",")
    fd.write(brand.replace("," , " ").replace("\n" , " "))
    fd.write(",")
    fd.write(img.replace("," , " ").replace("\n" , " "))
    fd.write(",")
    fd.write(price.replace("," , " ").replace("\n" , " "))
    fd.write(",")
    fd.write(discount.replace("," , " ").replace("\n" , " "))
    fd.write(",")
    fd.write(discount_perc.replace("," , " ").replace("\n" , " "))
    fd.write(",")
    fd.write(Weight.replace("," , " ").replace("\n" , " "))
    fd.write(",")
    fd.write(prod_details.strip().replace(",","").replace("\n" , "").replace("\r\n", "").replace("\t", "").replace("\r", ""))
    fd.write(",")
    categor = page_soup.find("div",{"class":"brcbs col16 -pts -pbm"}).findAll("a")
    for categ in categor:
        #print("test : " + categ.get_text())
        try:
            categ["href"]
        except:
            continue
        else:
            tex = categ.get_text()
            if "Home" in tex:
                continue
            else:
                print(tex)     
                fd.write(tex.replace("," , " ").replace("\n" , " "))
                fd.write(",")
                 
    fd.write("\n")            