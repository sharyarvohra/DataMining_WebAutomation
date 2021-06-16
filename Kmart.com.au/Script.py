import time
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as soup
import uuid
def Get_And_Write_Data(page_src,fd,page_url):
    page_soup=soup(page_src,"lxml")
    all_products = page_soup.findAll("div",{"class":"product product_box small-6 medium-4 large-4 columns clearfix col"})
    for product in all_products:
                title = product.find("p",{"class":"title"}).get_text().strip().replace(",","").replace("\n","")
                price = product.find("p",{"class":"price"}).get_text().strip().replace(",","").replace("\n","").replace("$","")
                if "WAS" in price:
                	orignal_price = price.split("WAS")[1]
                	discounted_Price = price.split("WAS")[0]
                else:
                	orignal_price = price
                	discounted_Price = "-"	


                img   = "https://www.kmart.com.au" +    product.find("img")["src"].replace("tf","sz").replace(",","").replace("\n","")
                product_url = "https://www.kmart.com.au"+product.find("a")["href"].replace(",","").replace("\n","")
                tags = product.find("div",{"class":"pdpMsgWrapper"}).get_text()
                try:
                	tt =  product.find("div",{"class":"roundel-wrapper"}).img
                	tt = "Just Landed ; "
                except:
                	tt = ";"	
                tags = tt + tags.strip()
                #rating = product.find("div",{"class":"standalone-bottomline"}).get_text().strip().split("star")[0]
                #reviews = product.find("div",{"class":"standalone-bottomline"}).a.get_text().strip().replace("Review","")	

                try:
                	rating = product.find("div",{"class":"standalone-bottomline"}).get_text().strip().split("star")[0]
                	reviews = product.find("div",{"class":"standalone-bottomline"}).a.get_text().strip().replace("Review","").replace("s","")
                	#print(rating)
                	#print(reviews)
                except:
                	rating = "Not Rated"
                	reviews = "0"	
                print(title)
                print("----------------------------------------------------------")

                product_uuid = str(uuid.uuid4())
                major_cateogry = categories[0]
                sub_category   = categories[len(categories)-1]

                fd.write(product_uuid.replace(",","").replace("\n",""))
                fd.write(",")
                fd.write(major_cateogry.replace(",","").replace("\n",""))
                fd.write(",")
                fd.write(page_url.replace(",","").replace("\n",""))
                fd.write(",")
                fd.write(sub_category.replace(",","").replace("\n",""))
                fd.write(",")
                fd.write(page_url.replace(",","").replace("\n",""))
                fd.write(",")
                fd.write(title.replace(",","").replace("\n",""))
                fd.write(",")
                fd.write(product_url.replace(",","").replace("\n",""))
                fd.write(",")   
                fd.write(img.replace(",","").replace("\n",""))
                fd.write(",")
                fd.write(price.replace(",","").replace("\n",""))
                fd.write(",")
                fd.write(discounted_Price.replace(",","").replace("\n",""))
                fd.write(",")
                fd.write(rating.replace(",","").replace("\n",""))
                fd.write(",")
                fd.write(reviews.replace(",","").replace("\n",""))
                fd.write(",")
                fd.write(tags)
                fd.write(",\n")



with open('link.csv','r') as csv_file:
    lines = csv_file.readlines()
urls = []
for line in lines:
    data = line.split(',')
    urls.append(data[0])


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--log-level=3")
driver = webdriver.Chrome(options=chrome_options,executable_path="chromedriver.exe") 	
for url in urls:
    url = url.replace("||",",")
    url = url + "#.plp-wrapper"
    print("Opeining URL: ",url)
    driver.get(url)
    time.sleep(2)
    #            #KmailSignupDisplay > div > div.modal-header.v2 > a
    try:
    	WebDriverWait(driver,7).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,"#KmailSignupDisplay > div > div.modal-header.v2 > a")))
    	driver.find_element_by_css_selector("#KmailSignupDisplay > div > div.modal-header.v2 > a").click()
    except:
    	zaada =1 
    try:
        WebDriverWait(driver,5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,'#widget_left_filter')))
    except:
        continue        	
    try:
        WebDriverWait(driver,7).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,"#show > div.switch-wrapper > a.ninety")))
        driver.find_element_by_css_selector("#show > div.switch-wrapper > a.ninety").click()
    except:
        try:
        	WebDriverWait(driver,5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,"#show > div.switch-wrapper > a.ninety.active")))
        except:
            zaada =1 	
    i = 2
    categories = driver.find_element_by_xpath('//*[@id="widget_breadcrumb"]').text.strip().replace("   ","|")
    categories = categories.split("|")
    categories.pop(0)
    previous = "NotAvailable"
    fd = open("["+categories[0].replace(" ","_")+"]_"+categories[len(categories)-1]+"_.csv","a",encoding = "utf-8") 
    try:
        while driver.find_element_by_css_selector("#WC_SearchBasedNavigationResults_pagination_link_right_categoryResults_bottom"):
            start = time.time()
            while 1:
                    end = time.time()
                    duration = end - start
                    if duration >=14:
                        driver.find_element_by_css_selector("#WC_SearchBasedNavigationResults_pagination_link_right_categoryResults_bottom").click()
                        print("Clicked.!")
                        time.sleep(2)
                    previous_orignal = driver.find_element_by_css_selector('#resultcontent > div:nth-child(1)').text.strip()
                    if previous_orignal != previous:
                        #print(previous_orignal)
                        Get_And_Write_Data(driver.page_source,fd,url)
                        break
                    else:
                        time.sleep(2)    
            previous = previous_orignal
            print("Navigating to Page=",i)
            i+=1
            element = driver.find_element_by_id('WC_SearchBasedNavigationResults_pagination_link_right_categoryResults_bottom')
            element.location_once_scrolled_into_view
            time.sleep(2)
            driver.find_element_by_css_selector("#WC_SearchBasedNavigationResults_pagination_link_right_categoryResults_bottom").click()
            print("Clicked.!")
            time.sleep(2)
            #print("Waited.!")    
    except:
        #print("Inexcepr")
        while 1:
                    previous_orignal = driver.find_element_by_css_selector('#resultcontent > div:nth-child(1)').text.strip()
                    if previous_orignal != previous:
                        #print(previous_orignal)
                        Get_And_Write_Data(driver.page_source,fd,url)
                        break
                    else:
                        time.sleep(2)    
        time.sleep(2)
driver.close()        
            	