#!/usr/bin/python3
import json
import sys
import time
import configparser
from selenium import webdriver
from logger import logging
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException


class Tools:

    def AddSet_var():
        global username
        global passwd
        global pro
        global country_list
        config = configparser.ConfigParser()
        config.read('config.ini')
        username = config.get('windscrib', 'user')
        passwd = config.get('windscrib', 'passwd')
        pro = config.getboolean('windscrib', 'pro')
        country_list = json.loads(config.get('windscrib', 'pro_num'))


    def make_UserAgent():
        user_agent = UserAgent(browsers=['chrome']).random
        logging.info(f'you are using {user_agent}')
        options.add_argument(f'user-agent=Mozilla/5.0 (X11; Linux i686; rv:90.0) Gecko/20100101 Firefox/90.0')

    def add_crxFile(address):
        assert isinstance(address, str), 'JUST SEND STR ADDRESS'
        options.add_extension(address)
    
    def click_exists(xpath):
        el = exists(xpath=xpath)
        el.check_exists()
        el.click_pr()

    def sendKey_exists(xpath, content):
        el = exists(xpath=xpath)
        el.check_exists()
        el.senKey_pr(content)

    def CheckText_exists(xpath, Base):
        el = exists(xpath=xpath)
        el.check_exists()
        t1 = el.check_text()
        if t1 == Base: return True
        return False
    
    def CheckPro_Cy(xpath):
        CY_div = driver.find_element(By.XPATH, xpath)
        try:
            element = CY_div.find_element(By.CLASS_NAME, 'css-1ky0bz0-FlagIcon')
            return False
        except NoSuchElementException:
            return True
        
    def Cy_check(num):
            xpath = f'//*[@id="app-frame"]/div/div[2]/div/div/div[{num}]'
            if Tools.CheckPro_Cy(xpath): return num

    def CheckPro_Dc(cy,nu):
        jscode = 'const targetXPath ='+ "'//*[@id="+f'"app-frame"]/div/div[2]/div/div/div[{cy}]/div[2]/div[{nu}]/div/div[2]/div[1]/div[3]/span[1]'+"';function findElementsByXPath(xpath) {const result = [];const nodesSnapshot = document.evaluate(xpath,document,null,XPathResult.ORDERED_NODE_SNAPSHOT_TYPE,null);for (let i = 0; i < nodesSnapshot.snapshotLength; i++) {result.push(nodesSnapshot.snapshotItem(i));}return result;}const targetElements = findElementsByXPath(targetXPath);if (targetElements.length > 0) {return 'Found'; } else {return 'Elements not found!';}"

        result = driver.execute_script(jscode)
        if result == 'Found': return False
        else: return True



    def DcNum_checkN(allCy):
        for cy in allCy:
            xpath = f'//*[@id="app-frame"]/div/div[2]/div/div/div[{cy}]'
            Tools.click_exists(xpath)
            elasli = driver.find_element(By.XPATH, xpath)
            DCs = elasli.find_elements(By.CLASS_NAME, 'css-1oh5hha-BaseListItem-DatacenterListItem')  
            for check_num in range(1, len(DCs) + 1):
                xxpath = f'//*[@id="app-frame"]/div/div[2]/div/div/div[{cy}]/div[2]/div[{check_num}]'
                try:
                    if Tools.CheckPro_Dc(cy, check_num): AllXpath[cy].append(xxpath)
                except:
                    if Tools.CheckPro_Dc(cy, check_num): AllXpath[cy] = [xxpath]
        
            
    def DcNum_checkP(allCy):
        for cy in allCy:
            xpath = f'//*[@id="app-frame"]/div/div[2]/div/div/div[{cy}]'
            Tools.click_exists(xpath)
            elasli = driver.find_element(By.XPATH, xpath)
            DCs = elasli.find_elements(By.CLASS_NAME, 'css-1oh5hha-BaseListItem-DatacenterListItem')
            for check_num in range(1, len(DCs) + 1):
                xxpath = f'//*[@id="app-frame"]/div/div[2]/div/div/div[{cy}]/div[2]/div[{check_num}]'
                try:
                    AllXpath[cy].append(xxpath)
                except:
                    AllXpath[cy] = [xxpath]

class exists:
    def __init__(self, xpath):
        self.xpath = xpath
        self.element = ''
    def check_exists(self):
        check = False
        while check == False:
            try:
                element = driver.find_element(By.XPATH, self.xpath)
                if element: check = True
                self.element = element
                time.sleep(0.5)
            except:
                continue

    def click_pr(self):
        driver.find_element(By.XPATH, self.xpath).click()

    def senKey_pr(self, content):
        driver.find_element(By.XPATH, self.xpath).send_keys(content)

    def check_text(self):
        return driver.find_element(By.XPATH, self.xpath).text



options = Options()
Tools.AddSet_var()
Tools.make_UserAgent()
Tools.add_crxFile('wind.crx')
driver = webdriver.Chrome(options=options, service_log_path='NUL')

driver.get("chrome-extension://hnmpcagpplmpfojmgmnngilcnanddlhb/popup.html")
Tools.click_exists('//*[@id="app-frame"]/div/button[2]')
Tools.sendKey_exists('//*[@id="app-frame"]/div/div/form/div[1]/div[2]/input', username)
Tools.sendKey_exists('//*[@id="app-frame"]/div/div/form/div[2]/div[2]/input', passwd)
time.sleep(0.5)
Tools.click_exists('//*[@id="app-frame"]/div/div/form/div[3]/button')
tl = Tools.CheckText_exists('//*[@id="app-frame"]/div/div[2]/div[1]', 'You Are Connected')
if tl != True: logging.warning('your opration go to err', extra={'debugLine': 'Line 95 - check string'});sys.exit()

Tools.click_exists('//*[@id="app-frame"]/div/button[2]')
Tools.click_exists('//*[@id="app-frame"]/div/div[4]/div[1]/div/div[1]/div/div[2]/button')

if pro: list_select = [num for num in range(country_list[0], country_list[1] + 1)]
else: list_select = [Tools.Cy_check(num) for num in range(country_list[0], country_list[1] + 1) if Tools.Cy_check(num) is not None]

AllXpath = {}
if pro: Tools.DcNum_checkP(list_select)
else: Tools.DcNum_checkN(list_select)


for vp in AllXpath:
        for vpl in AllXpath[vp]:
            print(vpl)
            Tools.click_exists(vpl)
            driver.execute_script("window.open('', '_blank');")
            driver.switch_to.window(driver.window_handles[1])
            driver.get("https://www.example.com")
            input()

input()
driver.close()
