from random import choice
import random
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem , Popularity
import requests
from bs4 import BeautifulSoup as soup
import time
import pandas
import urllib.request
#----------------------------Proxy Generator --------------------------------------------------------------
def proxy_generator(): 
    proxies = []
    response = requests.get("https://www.sslproxies.org/")
    soupp = soup(response.content, 'html5lib')
    proxies_table = soupp.find(id='proxylisttable')
    for row in proxies_table.tbody.find_all('tr'):
        proxies.append(row.findAll('td')[0].string +":"+row.findAll('td')[1].string)
    proxy = proxies[random.randint(0, len(proxies) - 1)]
    proxy = {"http":"https://"+str(proxy), "https":"https://"+str(proxy),"ftp":"ftp://"+str(proxy)}
    return proxy


popularity = [Popularity.COMMON.value, Popularity.POPULAR.value]
software_names = [SoftwareName.CHROME.value,SoftwareName.FIREFOX.value,SoftwareName.OPERA.value,SoftwareName.ANDROID.value]
operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value,OperatingSystem.MAC.value]
user_agent_rotator = UserAgent(software_names=software_names,popularity=popularity, operating_systems=operating_systems, limit=100)

#-----------------------------------------------------------------------------------------------------------------


#------------------------------------------Additional Details Function---------------------------------------------
def Additional_Details_Function_One(page_soup):
    details_container = []
    details = []
    try:
        page_soup.select("#prodDetails")[0].findAll("td",{"class":"label"})[1]
        page_soup.select("#prodDetails")[0].findAll("td",{"class":"value"})[1]
        for td in  page_soup.select("#prodDetails")[0].findAll("td",{"class":"label"}):
            details_container.append(td.get_text().strip())
        for td in  page_soup.select("#prodDetails")[0].findAll("td",{"class":"value"}):
            details.append(td.get_text().strip())  
    except:
        return False,None,None;
    else:
        return True,details_container,details;
def Additional_Details_Function_Two(page_soup):
        details_container = []
        details = []
        try:
            p=page_soup.select("#detail-bullets")[0].findAll("li")
        except:   
            return False,None,None;      
        for det in p:
            try:
                h = det.find("span",{"class":"a-text-bold"}).get_text().strip()
                i = det.find("span",{"class":"a-icon-alt"}).get_text().strip()
                det = h+i
            except:    
                det = det.get_text().strip().replace("," , "-").replace("\n" , "").replace("\t" , "")
                if det.find(':')==-1 or det.find("Best")!=-1:
                    continue 
            try:
                details_container.append(det.split(':')[:1][0].replace("," , "-").replace("  " , "").replace("\n" , "").replace("\t" , ""))
                details.append(det.split(':')[1:][0].replace("," , "-").replace("  " , "").replace("\n" , "").replace("\t" , ""))  
            except:
                continue
        return True,details_container,details;                       
def Additional_Details_Function_Three(page_soup):
    details_container = []
    details = []
    check =False
    try:
        page_soup.find("div",{"id":"prodDetails"}).find("tbody")
    except:
        return False,None,None;   
    else:
        p = page_soup.find("div",{"id":"prodDetails"})
        det_con = p.findAll("th",{"class":"a-color-secondary a-size-base prodDetSectionEntry"})
        det = p.findAll("td",{"class":"a-size-base"})
        for a in det_con:
            details_container.append(a.get_text().strip().replace("," , "-").replace("  " , "").replace("\n" , ""))
        for b in det:
            try:
                b.find("span",{"class":"a-icon-alt"}).get_text().strip()
            except:
                 details.append(b.get_text().strip())
            else:        
                details.append(b.find("span",{"class":"a-icon-alt"}).get_text().strip().replace("," , "-").replace("  " , "").replace("\n" , ""))

    return True,details_container,details;    

def Additional_Details_Function_Four(page_soup):
    details_container = []
    details = []
    try:
        p=page_soup.select("#detailBullets")[0].findAll("li")
    except:    
        return False,None,None;
    for det in p:
            try:
                h = det.find("span",{"class":"a-text-bold"}).get_text().strip()
                i = det.find("span",{"class":"a-icon-alt"}).get_text().strip()
                label = h+i
            except:
                try:    
                    h = det.findAll("span")
                    h[0].get_text().strip()

                except:
                    continue
                else:
                    label = h[0].get_text().strip()
                    if label.find(':')==-1 or label.find("Best")!=-1:
                        continue 
            try:
                details_container.append(label.split(':')[:1][0].replace("," , "-").replace("  " , "").replace("\n" , "").replace("\t" , ""))
                details.append(label.split(':')[1:][0].replace("," , "-").replace("  " , "").replace("\n" , "").replace("\t" , ""))  
            except:
                continue         
    return True,details_container,details;  

#---------------------------------------FILEREADING------------------------------------------
colnames = ['Column1']
Filename = "engagment+rings"
Filename_Link = Filename+".csv"
data = pandas.read_csv(Filename_Link, names=colnames)
urls  = data.Column1.tolist()

Filename_Details=Filename+"_Details.csv"
fd=open(Filename_Details,"a",encoding='utf-8')
headers="Product_URL,Product_Title,Category,Sub_Category,Sub_Sub_Category,Child_Category,Sub_Child_Category,Feature_One,Feature_Two,Feature_Three,Feature_Four,Feature_Five,Feature_Six,Feature_Seven,"
headers=headers+"Product_Price,Discount,Img_One,Img_Two,Img_Three,Img_Four,Img_Five,Img_Six,Img_Seven,Customer_Reviews,Product_Rating,Brand,Model,Item_Weight,Product_Dimensions,"
headers=headers+"Item_model_number,Manufacturer_Part_Number,Origin,ASIN,Shipping_Weight,OEM_Part_Number,Date_First_Available,"
headers=headers+"Additional_Detail_1,Additional_Detail_2,Additional_Detail_3,Additional_Detail_4,Additional_Detail_5,Additional_Detail_6"
headers=headers+"\n"
fd.write(headers)


Filename_Error="Error_.csv"
fe=open(Filename_Error,"a",encoding='utf-8')



itemscraped=0
you_have_proxy = False
got_result = False

for url in urls:
    #-----Headers----------------------------------------------------------------------------------------------
    ua =  user_agent_rotator.get_random_user_agent()   
    headers = {'User-Agent': ua}


    #------------Changing In URL---------------------------------------------------------------------------------
    #url = "https://www.amazon.com/dp/" + url


    #------------------------Request And Get Respone------------------------------------------------------------
    while 1:
        if you_have_proxy==False or got_result==False:
            you_have_proxy=False
            proxy = proxy_generator()
            ua =  user_agent_rotator.get_random_user_agent()
            print("Finding Proxy USerAgent")
            #print(str(proxy) + " "+ str(ua))
        try:
            page_html = requests.get(url,headers=headers,proxies=proxy,timeout=(5,10))
            you_have_proxy = True
            break
        except:
            got_result=False
            pass           
    page_soup = soup(page_html.content,features="lxml")

    print("Finding..!")

    #-----------------------------------CHECK RESPONESE---------------------------------------------------
    try:
        Product_Title= page_soup.select("#productTitle")[0].get_text().strip()
    except:
        print("url")
        fe.write(url + "\n")
        got_result=False
        continue
    #------------------------------------------Data Extration And CHECKS---------------------------------------------

    #-----------------------Categories----------------
    try:
        categories = []
        for li in page_soup.select("#wayfinding-breadcrumbs_container ul.a-unordered-list")[0].findAll("li"):
            categories.append(li.get_text().strip())
    except:
        categories="-"      
    #---------------Category------------------------------
    try:
        categories[0]
    except:
        Category="-"
    else:
        Category=categories[0]
    #---------------Sub_Category---------------------------
    try:
        categories[2]
    except:
        Sub_Category="-"
    else:
        Sub_Category=categories[2]    
    #---------------Sub_Sub_Category------------------------
    try:
        categories[4]
    except:
        Sub_Sub_Category="-"
    else:
        Sub_Sub_Category=categories[4]     
    #---------------Child Category---------------------------
    try:
        categories[6]
    except:
        Child_Category="-"
    else:
        Child_Category=categories[6]         
    #---------------Sub_Child_Category-----------------------
    try:
        categories[8]
    except:
        Sub_Child_Category="-"
    else:
        Sub_Child_Category=categories[8]     
    #-----------------------------------------------------------------------------------------------------------------------------------------------




    #------------------------------------------------------Fetaures Bullets Point -------------------------------------------------------------------
    try:
        features = []
        for li in page_soup.select("#feature-bullets ul.a-unordered-list")[0].findAll('li'):
            features.append(li.get_text().strip())
    except:
        print("")        
    try:
        features[0]
    except:
        Feature_One = "-"
    else:
        Feature_One= features[0]
    try:
        features[1]
    except:
        Feature_Two = "-"
    else:
        Feature_Two= features[1]
    try:
        features[2]
    except:
        Feature_Three = "-"
    else:
        Feature_Three= features[2]
    try:
        features[3]
    except:
        Feature_Four = "-"
    else:
        Feature_Four= features[3]
    try:
        features[4]
    except:
        Feature_Five = "-"
    else:
        Feature_Five= features[4]   
    try:
        features[5]
    except:
        Feature_Six = "-"
    else:
        Feature_Six= features[5]                
    try:
        features[6]
    except:
        Feature_Seven = "-"
    else:
        Feature_Seven= features[5]
    #--------------------------------------------------------------------------------------------------------------------------------    


    #--------------------------------------------------Product_Price -------------------------------------------------------
    try:
        page_soup.select("#priceblock_dealprice")[0].get_text().strip()
    except:
        try: 
            Product_Price=page_soup.select("#priceblock_ourprice")[0].get_text().strip()
            Discount="No"
        except:
            Discount="-"
            Product_Price = "Not Available" 
    else:
        Discount="Yes"
        Product_Price= page_soup.select("#priceblock_dealprice")[0].get_text().strip()
    #--------------------------------------------------------------------------------------------------------------------------------    
    

    #--------------------------------------------IMAGES_LINKS-----------------------------------------------------------------------------------
    img_link_container = page_soup.find("div",{"id":"altImages"})
    try:
        img_link_temp=img_link_container.findAll('img')
    except:
        fe.write(url + "\n")
        continue        
    img_link = []
    for link in img_link_temp:
        if "40_.jpg" in link["src"]:
            link["src"]=link["src"].replace("40_.jpg","300_.jpg")
            img_link.append(link["src"])
    try:        
        img_link[0] 
    except:
        Img_One = "-"
    else:
        Img_One = img_link[0]   

    try:        
        img_link[1] 
    except:
        Img_Two = "-"
    else:
        Img_Two = img_link[1] 

    try:        
        img_link[2] 
    except:
        Img_Three = "-"
    else:
        Img_Three = img_link[2] 

    try:        
        img_link[3] 
    except:
        Img_Four = "-"
    else:
        Img_Four = img_link[3] 

    try:        
        img_link[4] 
    except:
        Img_Five = "-"
    else:
        Img_Five = img_link[4]

    try:        
        img_link[5] 
    except:
        Img_Six = "-"
    else:
        Img_Six = img_link[5]  

    try:        
        img_link[6] 
    except:
        Img_Seven = "-"
    else:
        Img_Seven = img_link[6]

    #---------------------------------------------------------------------------------------------------------------------------------------------
    
    #-----------------------------------------------------All ADDITIONAL DETALS------------------------------------------------------------------
    details_container=[]
    details = []
    pos = 0

    result,details_container,details=Additional_Details_Function_One(page_soup)
    if result==False:
        result,details_container,details=Additional_Details_Function_Two(page_soup)
        if result==False:
            result,details_container,details=Additional_Details_Function_Three(page_soup)
            if result==False:
                result,details_container,details=Additional_Details_Function_Four(page_soup)           
    #-------------------Reviews And Rating-----------------------------------------
    try:
        Product_Rating = page_soup.find("span",{"data-hook":"rating-out-of-text"}).get_text().strip()
        Customer_Reviews =page_soup.find("div",{"data-hook":"total-review-count"}).get_text().strip() 
    except:
        Product_Rating = "Not Rated"
        Customer_Reviews = "0 Ratings"   

    #---------------Brand-----------------------------------------------------------------------
    try:
        pos=details_container.index('Brand')
    except:
        Brand="-"
    else:
        Brand=details[pos]    
    #------------------------Model-----------------------------------------------------------------
    try:
        pos=details_container.index('Model')
    except:
        Model="-"
    else:
        Model=details[pos]
    #----------------------Item Weight------------------------------
    try:
        pos=details_container.index('Item Weight')
    except:
        Item_Weight="-"
    else:
        Item_Weight=details[pos]
    #----------------------Product Dimensions-----------------------------------------------
    try:
        pos=details_container.index('Product Dimensions')
    except:
        Product_Dimensions="-"
    else:
        Product_Dimensions=details[pos]   
    #-------------------------Item_Model_)Number-----------------------------  
    try:
        pos=details_container.index('Item model number')
    except:
        Item_model_number="-"
    else:
        Item_model_number=details[pos]     
    #------------------------Manufacturer Part Number-----------------------------  
    try:
        pos=details_container.index('Manufacturer Part Number')
    except:
        Manufacturer_Part_Number="-"
    else:
        Manufacturer_Part_Number=details[pos]
    #------------------------ASINr-----------------------------  
    try:
        pos=details_container.index('ASIN')
    except:
        ASIN="-"
    else:
        ASIN=details[pos]  
    #------------------------Origin-----------------------------  
    try:
        pos=details_container.index('Origin')
    except:
        Origin="-"
    else:
        Origin=details[pos] 
    #------------------------Shipping Weight-----------------------------  
    try:
        pos=details_container.index('Shipping Weight')
    except:
        Shipping_Weight="-"
    else:
        Shipping_Weight=details[pos]
    #------------------------OEM Part Number-----------------------------  
    try:
        pos=details_container.index('OEM Part Number')
    except:
        OEM_Part_Number="-"
    else:
        OEM_Part_Number=details[pos]    
    #------------------------Date First Available---------------------------- 
    try:
        pos=details_container.index('Date First Available')
    except:
        Date_First_Available="-"
    else:
        Date_First_Available=details[pos] 

    #---------------------------------------------------Additional Details Column------------------------------------------------------------------------------------- 
    #------------------------Additional Detail 1---------------------------- 
    try:
        pos=details_container.index('Additional Detail 1')
    except:
        Additional_Detail_1="-"
    else:
        Additional_Detail_1=details[pos]       
    #------------------------Additional Detail 2---------------------------- 
    try:
        pos=details_container.index('Additional Detail 2')
    except:
        Additional_Detail_2="-"
    else:
        Additional_Detail_2=details[pos]
    #------------------------Additional Detail 3---------------------------- 
    try:
        pos=details_container.index('Additional Detail 3')
    except:
        Additional_Detail_3="-"
    else:
        Additional_Detail_3=details[pos]
    #------------------------Additional Detail 4---------------------------- 
    try:
        pos=details_container.index('Additional Detail 4')
    except:
        Additional_Detail_4="-"
    else:
        Additional_Detail_4=details[pos]
    #------------------------Additional Detail 5---------------------------- 
    try:
        pos=details_container.index('Additional Detail 5')
    except:
        Additional_Detail_5="-"
    else:
        Additional_Detail_5=details[pos]
    #------------------------Additional Detail 6---------------------------- 
    try:
        pos=details_container.index('Additional Detail 7')
    except:
        Additional_Detail_6="-"
    else:
        Additional_Detail_6=details[pos]                    

    #------------------------------------------------------------------------------------------------------------------------------------------------    

    got_result=True

    #-----------------------------------------------Print Details--------------------------------------------------------------------------------------

    print("Product_URL:"+url.replace("," , "-").replace("\n" , " "))
    print("Product_Title:"+Product_Title.replace("," , "-").replace("\n" , " "))
    print("Category:"+Category.replace("," , "-").replace("\n" , " "))
    print("Sub_Category:"+ Sub_Category.replace("," , "-").replace("\n" , " "))
    print("Sub_Sub_Category:"+ Sub_Sub_Category.replace("," , "-").replace("\n" , " "))
    print("Child_Category:"+Child_Category.replace("," , "-").replace("\n" , " "))
    print("Sub_Child_Category:"+Sub_Child_Category.replace("," , "-").replace("\n" , " "))
    print("Feature_One:"+Feature_One.replace("," , "-").replace("\n" , " "))
    print("Feature_Two:"+Feature_Two.replace("," , "-").replace("\n" , " "))
    print("Feature_Three:"+Feature_Three.replace("," , "-").replace("\n" , " "))
    print("Feature_Four:"+Feature_Four.replace("," , "-").replace("\n" , " "))
    print("Feature_Five:"+Feature_Five.replace("," , "-").replace("\n" , " "))
    print("Feature_Six:"+Feature_Six.replace("," , "-").replace("\n" , " "))
    print("Feature_Seven:"+Feature_Seven.replace("," , "-").replace("\n" , " "))
    print("Product_Price:"+Product_Price.replace("," , "-").replace("\n" , " "))
    print("Discount:"+Discount.replace("," , "-").replace("\n" , " "))
    print("Img_One:"+Img_One.replace("," , "-").replace("\n" , " "))
    print("Img_Two:"+Img_Two.replace("," , "-").replace("\n" , " "))
    print("Img_Three:"+Img_Three.replace("," , "-").replace("\n" , " "))
    print("Img_Four:"+Img_Four.replace("," , "-").replace("\n" , " "))
    print("Img_Five:"+Img_Five.replace("," , "-").replace("\n" , " "))
    print("Img_Six:"+Img_Six.replace("," , "-").replace("\n" , " "))
    print("Img_Seven:"+Img_Seven.replace("," , "-").replace("\n" , " "))
    print("Customer_Reviews:"+Customer_Reviews.replace("," , "-").replace("\n" , " "))
    print("Product_Rating:"+Product_Rating.replace("," , "-").replace("\n" , " "))
    print("Brand:"+Brand.replace("," , "-").replace("\n" , " "))
    print("Model:"+Model.replace("," , "-").replace("\n" , " "))
    print("Item_Weight:"+Item_Weight.replace("," , "-").replace("\n" , " "))
    print("Product_Dimensions:"+Product_Dimensions.replace("," , "-").replace("\n" , " "))
    print("Item_model_number:"+Item_model_number.replace("," , "-").replace("\n" , " "))
    print("Manufacturer_Part_Number:"+Manufacturer_Part_Number.replace("," , "-").replace("\n" , " "))
    print("Origin:"+Origin.replace("," , "-").replace("\n" , " "))
    print("ASIN:"+ASIN.replace("," , "-").replace("\n" , " "))
    print("Shipping_Weight:"+Shipping_Weight.replace("," , "-").replace("\n" , " "))
    print("OEM_Part_Number:"+OEM_Part_Number.replace("," , "-").replace("\n" , " "))
    print("Date_First_Available:"+Date_First_Available.replace("," , "-").replace("\n" , " "))
    print("Additional_Detail_1:"+Additional_Detail_1.replace("," , "-").replace("\n" , " "))
    print("Additional_Detail_2:"+Additional_Detail_2.replace("," , "-").replace("\n" , " "))
    print("Additional_Detail_3:"+Additional_Detail_3.replace("," , "-").replace("\n" , " "))
    print("Additional_Detail_4:"+Additional_Detail_4.replace("," , "-").replace("\n" , " "))
    print("Additional_Detail_5:"+Additional_Detail_5.replace("," , "-").replace("\n" , " "))
    print("Additional_Detail_6:"+Additional_Detail_6.replace("," , "-").replace("\n" , " "))

    #-----------------------------------------------------------------------------------WRITING IN FILE--------------------------------------------------------------------------
    
    fd.write(url.replace("," , "-").replace("\n" , " "))
    fd.write(",")
    fd.write(Product_Title.replace("," , "-").replace("\n" , " "))
    fd.write(",") 
    fd.write(Category.replace("," , "-").replace("\n" , " "))
    fd.write(",")
    fd.write(Sub_Category.replace("," , "-").replace("\n" , " "))
    fd.write(",")
    fd.write( Sub_Sub_Category.replace("," , "-").replace("\n" , " "))
    fd.write(",")
    fd.write(Child_Category.replace("," , "-").replace("\n" , " "))
    fd.write(",")
    fd.write(Sub_Child_Category.replace("," , "-").replace("\n" , " "))
    fd.write(",")
    fd.write(Feature_One.replace("," , "-").replace("\n" , " "))
    fd.write(",")
    fd.write(Feature_Two.replace("," , "-").replace("\n" , " "))
    fd.write(",")
    fd.write(Feature_Three.replace("," , "-").replace("\n" , " "))
    fd.write(",")
    fd.write(Feature_Four.replace("," , "-").replace("\n" , " "))
    fd.write(",")
    fd.write(Feature_Five.replace("," , "-").replace("\n" , " "))
    fd.write(",")
    fd.write(Feature_Six.replace("," , "-").replace("\n" , " "))
    fd.write(",")
    fd.write(Feature_Seven.replace("," , "-").replace("\n" , " "))
    fd.write(",")
    fd.write(Product_Price.replace("," , "-").replace("\n" , " "))
    fd.write(",")
    fd.write(Discount.replace("," , "-").replace("\n" , " "))
    fd.write(",")
    fd.write(Img_One.replace("," , "-").replace("\n" , " "))
    fd.write(",")
    fd.write(Img_Two.replace("," , "-").replace("\n" , " "))
    fd.write(",")
    fd.write(Img_Three.replace("," , "-").replace("\n" , " "))
    fd.write(",")
    fd.write(Img_Four.replace("," , "-").replace("\n" , " "))
    fd.write(",")
    fd.write(Img_Five.replace("," , "-").replace("\n" , " "))
    fd.write(",")
    fd.write(Img_Six.replace("," , "-").replace("\n" , " "))
    fd.write(",")
    fd.write(Img_Seven.replace("," , "-").replace("\n" , " "))
    fd.write(",")
    fd.write(Customer_Reviews.replace("," , "-").replace("\n" , " "))
    fd.write(",")
    fd.write(Product_Rating.replace("," , "-").replace("\n" , " "))
    fd.write(",")
    fd.write(Brand.replace("," , "-").replace("\n" , " "))
    fd.write(",")
    fd.write(Model.replace("," , "-").replace("\n" , " "))
    fd.write(",")
    fd.write(Item_Weight.replace("," , "-").replace("\n" , " "))
    fd.write(",")
    fd.write(Product_Dimensions.replace("," , "-").replace("\n" , " "))
    fd.write(",")
    fd.write(Item_model_number.replace("," , "-").replace("\n" , " "))
    fd.write(",")
    fd.write(Manufacturer_Part_Number.replace("," , "-").replace("\n" , " "))
    fd.write(",")
    fd.write(Origin.replace("," , "-").replace("\n" , " "))
    fd.write(",")
    fd.write(ASIN.replace("," , "-").replace("\n" , " "))
    fd.write(",")
    fd.write(Shipping_Weight.replace("," , "-").replace("\n" , " "))
    fd.write(",")
    fd.write(OEM_Part_Number.replace("," , "-").replace("\n" , " "))
    fd.write(",")
    fd.write(Date_First_Available.replace("," , "-").replace("\n" , " "))
    fd.write(",")
    fd.write(Additional_Detail_1.replace("," , "-").replace("\n" , " "))
    fd.write(",")
    fd.write(Additional_Detail_2.replace("," , "-").replace("\n" , " "))
    fd.write(",")
    fd.write(Additional_Detail_3.replace("," , "-").replace("\n" , " "))
    fd.write(",")
    fd.write(Additional_Detail_4.replace("," , "-").replace("\n" , " "))
    fd.write(",")
    fd.write(Additional_Detail_5.replace("," , "-").replace("\n" , " "))
    fd.write(",")
    fd.write(Additional_Detail_6.replace("," , "-").replace("\n" , " "))
    fd.write("\n")
    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------










