import base64
import time
import pandas as pd
import requests
import json
import random
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import selenium.webdriver.support.ui as ui
from webdriver_manager.chrome import ChromeDriverManager
from pyvirtualdisplay import Display

class checkUrl():
    def __init__(self):
        self.driver = self.driverInit()
        self.wait = ui.WebDriverWait(self.driver, timeout=10000)
        self.url_checked = {}
        self.last_inFile = 2808

    
    def driverInit(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--headless")
        # chrome_options.add_argument("--disable-dev-shm-usage")
        # chrome_options.add_argument("--no-sandbox")
        # prefs = {
        #     "download.default_directory" : "D:\\Perso",
        #     "download.prompt_for_download": False,
        #     "download.directory_upgrade": True,
        #     "plugins.always_open_pdf_externally": True
        #     }
        # chrome_options.add_experimental_option("prefs",prefs)
        # chrome_options.page_load_strategy = 'normal'
        webdriver.Chrome(ChromeDriverManager().install())
        screen  = Display(visible=0, size=(1920,1081)).start()
        driver = webdriver.Chrome(executable_path="//usr//local//bin//chromedriver",chrome_options=chrome_options)
        return driver
        
    def filesData (self,osFiles):
        dataFile = pd.read_excel(osFiles)
        all_id = dataFile.loc[:,"id"].tolist()
        url = " http://51.210.181.193:5009/api/creativities/details"
        for id in all_id:
            print(id)
            if id > self.last_inFile:
                data_post = {
                    "user_id": 52,
                    "apikey": "ohaQzT-OXQJaP-hZlVoU-CoMkhN-vK5UPZ",
                    "creaid": id
                }
                req = requests.post(url,data=data_post)
                konti_data = json.loads(req.text)
                self.decode(konti_data[0]['original'], dataFile.copy(), id)
                print("--"*65)
        
        
    def decode(self,code, file_data, indice):
        status = "error"
        html = base64.b64decode(code)
        soup = BeautifulSoup(html, "html.parser")
        if soup.find("a") != None:
            # print(soup.find_all("a"))
            # print("----------4552245")
            sub_link =soup.find("a")
            try:
                rand_link = sub_link["href"]
            except Exception as e:
                print(e,"-------------################# ERROR #############")
                print(type(e))
                if type(e) == KeyError:
                    all_link = soup.find_all("a")
                    sub_link = random.choice(all_link)
                    print(sub_link)
                    try:
                        print(0)
                        rand_link = sub_link["href"]
                    except Exception as ex:
                        print(ex,"-------------################# ERROR 2 #############")
                        try:
                            if type(ex) == KeyError:
                                self.decode(code, file_data, indice)
                        except RecursionError :
                            rand_link = ""
                else:
                    rand_link = sub_link.find("a")["href"]
        elif soup.find("a") == None:
            rand_link = ""
        print('LINK --------------')
        print(rand_link)
        newdata = file_data[file_data["id"] == indice]
        # newdata = file_data[file_data["id"] == 144]
        newdata.loc[:,'link'] = rand_link
        try:
            # check = requests.get(url=rand_link, headers=headers, timeout=5, allow_redirects=False)
            if rand_link not in self.url_checked and rand_link != "":
                self.driver.get(rand_link)
                self.wait.until(EC.presence_of_all_elements_located((By.XPATH, "/html/body")))
                page_load = self.driver.page_source
                bodySoup = BeautifulSoup(page_load, "html.parser")
                body_img = bodySoup.find_all("img")
                print(len(body_img), "img ------")
                if len(body_img) > 0:
                    status = "success"
                else:
                   status = "error"
            elif rand_link in self.url_checked and rand_link != "":
                print("ALREADY IN")
                status = self.url_checked[rand_link]
            elif rand_link == "":
                status = "ERROR IN DATA "
        except Exception as e:
            status = "error"
        newdata.loc[:,'status'] = status
        self.url_checked[rand_link]=status
        newdata.to_csv('files/result.csv', sep=';', mode='a', index =False, header=False)
    
file_path = "files/exports2.xlsx"
check = checkUrl()
check.filesData(file_path) 