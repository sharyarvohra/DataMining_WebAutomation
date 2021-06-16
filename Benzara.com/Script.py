import requests
from bs4 import BeautifulSoup as soup
import time
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")
#chrome_options.add_argument("--headless")
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
chrome_options.add_argument("--log-level=3")
chrome_options.binary_location = r"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
driver = webdriver.Chrome(options=chrome_options,executable_path="chromedriver.exe")
fe = open("error.csv","a")

with open('Links.csv','r') as csv_file:
    lines = csv_file.readlines()
urls = []
for line in lines:
    data = line.split(',')
    urls.append(data[0])

email = "heather.mackey@infinitydesignliving.com"
password = "kBinZzvg@69xxni"
driver.get("https://benzara.com/account/login")
WebDriverWait(driver,5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,"#customer_email")))
driver.find_element_by_css_selector('#customer_email').send_keys(email)
driver.find_element_by_css_selector('#customer_password').send_keys(password)
driver.find_element_by_css_selector('#customer_login > input.btn.action_button').click()
time.sleep(4)

Filename_Details = "Observation_Details.csv"
fd = open(Filename_Details, "a",encoding='utf-8-sig')
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'}  
#fd.write("Handle,Title,Body (HTML),Vendor,Tags,Cost Per Item,Variant Price,Variant Compare At Price,Status,Option1 Name,Option1 Value,Option2 Name,Option2 Value,Option3 Name,Option3 Value,Variant SKU,Variant Grams,Image Src,Variant Image 2,Variant Image 3,Variant Image 4,Variant Image 5,Variant Image 6,Variant Image 7,Variant Image 8,Variant Image 9\n")
for url,i in zip(urls,range(1,100000000000000000)):
	    if i <= 6078:
	    	continue
	    driver.get(url)
	    try:
	    	WebDriverWait(driver,5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,"body > div.container.main.content > div:nth-child(2) > div > div.section.product_section.clearfix.js-product_section > div.seven.columns.omega > h1")))
	    except:
	    	fe.write(url+"\n")
	    	print("Product Id :    ",i)
	    	print('------------------------------------------')
	    	continue
	    page_soup = soup(driver.page_source,features="lxml")
	    title = page_soup.find("h1",{"class":"product_name"}).get_text().strip()
	    handle = title.lower().replace(" ","-")
	    Cost_Per_Item = page_soup.find('span',{"itemprop":"price"})["content"].replace(",","").replace("\n","")
	    Variant_Price = round(float(page_soup.find('span',{"itemprop":"price"})["content"].replace(",","").replace("\n",""))/0.4,2)
	    Compare_At_Price = str(round(float((Variant_Price * 0.60)+ Variant_Price),2))
	    Variant_Price = str(Variant_Price)
	    Out_of_Stock = page_soup.find("span",{"class":"sold_out"}).get_text().strip()
	    try:
	    	weight = page_soup.find('form',{"action":"/cart/add"})["data-product"].split('weight":')[1].split(",")[0]
	    except:
	    	weight = "0"	
	    if Out_of_Stock == "":
	    	Out_of_Stock = "active"
	    else:
	    	Out_of_Stock = "draft"	
	    sku   = page_soup.find("span",{"itemprop":"sku"}).get_text()
	    try:
	    	description = "<p>"+page_soup.find("div",{"itemprop":"description"}).get_text().strip()+"</p>"
	    except:
	    	description = 	"<p>"+"</p>"
	    color = ""
	    dimension = ""
	    material = ""	
	    try:	
	    	swatch = page_soup.find("div",{"class":"swatch_options"}).findAll("div",{"class":"swatch clearfix"})
	    	for option in swatch:
	    		if "color" in option.get_text().lower():
	    			color = option.input["value"] 
	    		if "dimension" in option.get_text().lower():
	    			dimension = option.input["value"] 
	    		if "material" in option.get_text().lower():
	    			material = option.input["value"] 	
	    except:
	    	()			
	    all_image = page_soup.find("div",{"class":"slick-track"}).findAll("img")
	    print("Product Id :    ",i)
	    print(handle)
	    print(title)
	    print(sku)
	    print(dimension)
	    print(color)
	    print(material)
	    print(Variant_Price)


	    fd.write(handle.replace(",","").replace("\n",""))
	    fd.write(",")
	    fd.write(title.replace(",","").replace("\n",""))
	    fd.write(",")
	    fd.write(description.replace(",","  ").replace("\n","    "))
	    fd.write(",")
	    fd.write("Benzara")
	    fd.write(",")
	    fd.write("_Benzara Wholesale")
	    fd.write(",")
	    fd.write(Cost_Per_Item.replace(",","").replace("\n",""))
	    fd.write(",")
	    fd.write(Variant_Price.replace(",","").replace("\n",""))
	    fd.write(",")
	    fd.write(Compare_At_Price.replace(",","").replace("\n",""))
	    fd.write(",")
	    fd.write(Out_of_Stock.replace(",","").replace("\n",""))
	    fd.write(",")
	    if color != "":
	    	fd.write("Color")
	    	fd.write(",")
	    	fd.write(color.replace(",","").replace("\n",""))
	    	fd.write(",")
	    else:
	    	fd.write("")
	    	fd.write(",")
	    	fd.write("")
	    	fd.write(",")
	    if dimension != "":	
	    	fd.write("Dimension")
	    	fd.write(",")
	    	fd.write(dimension.replace(",","").replace("\n",""))
	    	fd.write(",")
	    else:
	    	fd.write("")
	    	fd.write(",")
	    	fd.write("")
	    	fd.write(",")
	    if material !="":
	    	fd.write("Material")
	    	fd.write(",")
	    	fd.write(material.replace(",","").replace("\n",""))
	    	fd.write(",")
	    else:
	    	fd.write("")
	    	fd.write(",")
	    	fd.write("")
	    	fd.write(",") 	
	    fd.write(sku.replace(",","").replace("\n",""))
	    fd.write(",")
	    fd.write(weight.replace(",","").replace("\n",""))
	    fd.write(",")
	    for image in all_image:	
	    	fd.write("https:"+image["src"].replace(",","").replace("\n",""))
	    	fd.write(",")
	    	print("https:"+image["src"])
	    fd.write("\n")	

	    print('---------------------------------------')

