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
        if pro: country_list = json.loads(config.get('windscrib', 'pro_num'))
        else: country_list = json.loads(config.get('windscrib', 'normal_num'))
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




# pro
# //*[@id="app-frame"]/div/div[2]/div/div/div[2]



options = Options()
Tools.AddSet_var()
Tools.make_UserAgent()
Tools.add_crxFile('wind.crx')
driver = webdriver.Chrome(options=options, service_log_path='NUL')

driver.get("chrome-extension://hnmpcagpplmpfojmgmnngilcnanddlhb/popup.html")
Tools.click_exists('//*[@id="app-frame"]/div/button[2]')
Tools.sendKey_exists('//*[@id="app-frame"]/div/div/form/div[1]/div[2]/input', username)
Tools.sendKey_exists('//*[@id="app-frame"]/div/div/form/div[2]/div[2]/input', passwd)
time.sleep(2)
Tools.click_exists('//*[@id="app-frame"]/div/div/form/div[3]/button')
tl = Tools.CheckText_exists('//*[@id="app-frame"]/div/div[2]/div[1]', 'You Are Connected')
if tl != True: logging.warning('your opration go to err', extra={'debugLine': 'Line 95 - check string'});sys.exit()

Tools.click_exists('//*[@id="app-frame"]/div/button[2]')
Tools.click_exists('//*[@id="app-frame"]/div/div[4]/div[1]/div/div[1]/div/div[2]/button')
if pro: list_select = [num for num in range(country_list[0], country_list[1] + 1)]
else: list_select = country_list

print(list_select)
mydiv = driver.find_element(By.XPATH, '//*[@id="app-frame"]/div/div[2]/div/div/div[2]')
Tools.click_exists('//*[@id="app-frame"]/div/div[2]/div/div/div[2]')
time.sleep(1)
children = mydiv.find_elements(By.XPATH, '*')

# Itertae over the children
for child in children:
    print("\nChild Element")
    print(child.get_attribute('outerHTML'))

input()
driver.close()