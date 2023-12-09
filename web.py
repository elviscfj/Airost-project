from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import os
from bs4 import BeautifulSoup
import pandas as pd

class Web(webdriver.Chrome):
    
    def __init__(self, driver_path = r'C:\python\web scrap\chrome-win64') :
        self.driver_path = driver_path
        os.environ['PATH'] += self.driver_path
        option = webdriver.ChromeOptions()
        option.add_argument('--headless')
        super(Web, self).__init__()
        self.implicitly_wait(9999999)
        self.maximize_window()
    
    def main(self):

        #Launch website
        wait = WebDriverWait(self, 30)
        search_term = input("keyword : ")
        baselink = "https://www.shopee.my/search?keyword="
        search_term = search_term.replace(' ', '+')
        link = baselink + search_term
        self.get(link)
        time.sleep(10)
        
        #Set language, close language popout
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='English']"))).click()
        time.sleep(15)

        #Login
        username = input('Username:')
        pw = input('Password: ')
        WebDriverWait(self, 10).until(EC.presence_of_element_located((By.NAME, "loginKey")))
        self.find_element(By.NAME, "loginKey").send_keys(username)
        self.find_element(By.NAME, 'password' ).send_keys(pw)
        time.sleep(5)
        self.find_element(By.NAME, 'password' ).send_keys(Keys.ENTER)
        time.sleep(10)

        
    def scrap(self):

        content = self.page_source
        soup = BeautifulSoup(content, 'html.parser')
        time.sleep(60)

        for item in soup.find_all('div', class_ = 'col-xs-2-4 shopee-search-item-result__item'):
            
            name = item.find('div',class_ = 'GD02sl _3AO1tA IXhE9E').get_text(strip = True)
            print(name)
        
            if (item.find('div', class_ = 'jA9u-g F6VmiT')):
                price = item.find('span', class_ = 'P3wxsv').text.strip() + item.find('span', class_ = 'sHnxNa').text.strip()
            price = item.find('div', class_ = 'jA9u-g _4hzjIJ bD2oNb').get_text(strip = True)
            plink = item.find('a')['href']
                
            try:
                sold = item.find('div', class_ = 'sdJLPr MbhsP1').get_text(strip = True)
            except:
                sold = 'No item sold'

            productlist = []
            product = {
                'name' : name,
                'price' : price,
                'product link' : plink,
                'item sold' : sold
                }

            productlist.append(product)

            #put data in dataframe and output data
            df = pd.DataFrame(productlist)
            print(df.head(15))

            

            






       

   


    







