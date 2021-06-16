from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as soup
import time

import os

fd = open("Full inventory Image Details.csv","a")
fd.write("Title,Static Image Link\n")

#--------------------- Setting Chrome Driver--------------------------------------
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
chrome_options.add_argument("--log-level=3")
chrome_options.binary_location = r"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
driver = webdriver.Chrome(options=chrome_options,executable_path="chromedriver.exe")
#----------------------------------------------------------------------------------------------------


#------------------ Login To Account------------------------------------
driver.get("https://identity.flickr.com/login?redir=%2Fphotos%2Fupload%2F")
WebDriverWait(driver,5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,"#login-email")))
driver.find_element_by_css_selector('#login-email').send_keys("emailhere")
driver.find_element_by_css_selector('#login-form > button').click()
WebDriverWait(driver,5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,"#login-password")))
driver.find_element_by_css_selector('#login-password').send_keys("passwordhere")
driver.find_element_by_css_selector('#login-form > button').click()
WebDriverWait(driver,10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,"#upload-cr")))
#----------------------------------------------------------------------------------------

i = 1
for filename in os.listdir("DirectoryHere"+os.getcwd()):
    if filename.endswith(".png") or filename.endswith(".jpg") or filename.endswith(".jpeg"): 
    	driver.find_element_by_css_selector("#choose-photos-and-videos").send_keys(os.getcwd()+"\\"+filename)
    	i+=1
    	time.sleep(1)
    else:
        continue
time.sleep(3)
driver.find_element_by_css_selector('#action-publish').click()
WebDriverWait(driver,5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,"#confirm-publish")))
driver.find_element_by_css_selector('#confirm-publish').click()
WebDriverWait(driver,100).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,"#content")))
time.sleep(10)
page_html = driver.page_source
page_soup = soup(page_html,"lxml")
all_links = page_soup.find("div",{"class":"view photo-list-view requiredToShowOnServer photostream"}).findAll("div",{"class":"view photo-list-photo-view requiredToShowOnServer photostream awake"})
for link,z in zip(all_links,range(1,i)):
	url = link["style"].split("//")[1].replace('");','')
	print(link.find("div",{"class":"text"}).a.get_text(),end='  ')
	print(url)
	fd.write(link.find("div",{"class":"text"}).a.get_text().replace(",","").replace("\n","").replace("\r","")+",")
	fd.write(url+"\n")

driver.quit()