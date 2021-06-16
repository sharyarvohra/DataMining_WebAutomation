from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

Filename_Details= 	"EviveCare_Details.csv"
fd=open(Filename_Details,"a",encoding='utf-8-sig')
fd.write("\n")
fd.write("Product URL ,Product Title,Orange Price,Grey Price(Original Price),Discount,Image Url,Reviews,Product Bought,Rating By Customer,Date Of review \n")

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--log-level=3")
driver = webdriver.Chrome(chrome_options=chrome_options,executable_path="chromedriver.exe")    

with open('dataminer.csv','r') as csv_file:
    lines = csv_file.readlines()
urls = []
for line in lines:
    data = line.split(',')
    urls.append(data[0])
 
for url in urls:
    driver.get(url)
    time.sleep(7)
    review_csv=[]
    product_csv = []
    rating_csv =[]
    date_review_csv = []
    titles = driver.find_element_by_class_name('pdp-mod-product-badge-title').text
    orange_price = driver.find_element_by_xpath('//*[@id="module_product_price_1"]/div/div/span').text
    try:
    	grey_price = driver.find_element_by_xpath('//*[@id="module_product_price_1"]/div/div/div/span[1]').text
    	discount = driver.find_element_by_xpath('//*[@id="module_product_price_1"]/div/div/div/span[2]').text
    except:
    	grey_price = "-"	
    	discount = "-"
    image = driver.find_element_by_xpath('//*[@id="module_item_gallery_1"]/div/div[1]/div/img').get_attribute("src")
    image = str(image).replace("_.webp","")
    while True:
          #Get the review details here
          try:
            WebDriverWait(driver,10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,"div.item")))
          except:
          	  review_csv.append("-")
          	  product_csv.append("-")
          	  rating_csv.append("-")
          	  date_review_csv.append("-")
          	  break;
          product_reviews = driver.find_elements_by_css_selector("[class='item']")    

          # Get product review
          for product in product_reviews:    

              review = product.find_element_by_css_selector("[class='content']").text
              if (review != "" or review.strip()):
                  review_csv.append(review)
              else:
                  review_csv.append("No comments/review is an image")    

              # Product Purchase
              # Check if the product purchase exists    
              try:
              	product_purchase = product.find_element_by_css_selector("[class='skuInfo']").text
              	product_csv.append(product_purchase)    
              except:
              	product_csv.append("No Specified")	
              # Star rating
              star_ratings = product.find_elements_by_css_selector("[class='star']")
              stars = "https://laz-img-cdn.alicdn.com/tfs/TB19ZvEgfDH8KJjy1XcXXcpdXXa-64-64.png"    

              star_rate = 0
              for rating in star_ratings:
                  # print(rating.get_attribute('src'))
                  if (rating.get_attribute('src') == stars):
                      star_rate = star_rate + 1
              if star_rate == 0:
              	star_rate = "Not Rated."        
              rating_csv.append(star_rate)    

              # Date of Review
              date = product.find_element_by_css_selector("[class='title right']").text
              date_review_csv.append(date)    

          #Check for button next-pagination-item have disable attribute then jump from loop else click on the next button
          if len(driver.find_elements_by_css_selector("button.next-pagination-item.next[disabled]"))>0:
              break;
          else:
            try:
                button_next=WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button.next-pagination-item.next")))
                driver.execute_script("arguments[0].click();", button_next)
                print("next page")
                time.sleep(2)    

            except:
                break;  	

    for sreview,sproduct,sreview_star,sreview_date in zip(review_csv,product_csv,rating_csv,date_review_csv):
    	print("URL : " + url.replace("," , "-").replace("\n" , " "))
    	print("Title : " + titles.replace("," , "-").replace("\n" , " "))
    	print("Orange_Price : "+orange_price.replace("," , "-").replace("\n" , " "))
    	print("grey_price : "+grey_price.replace("," , "-").replace("\n" , " ") )
    	print("Discount : " + discount.replace("," , "-").replace("\n" , " "))
    	print("Review:"+ sreview.replace("," , "-").replace("\n" , " ") )
    	print("Review Product : " + sproduct.replace("," , "-").replace("\n" , " "))
    	print("Review Star : "+str(sreview_star).replace("," , "-").replace("\n" , " "))
    	print("Review Date : " + str(sreview_date).replace("," , "-").replace("\n" , " "))

driver.close()