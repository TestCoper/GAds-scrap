#!/usr/bin/python3
from selenium import webdriver
from .logger import logging
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options



def make_UserAgent():
    user_agent = UserAgent().random
    logging.info(f'you are using {user_agent}')
    options.add_argument(f'user-agent={user_agent}')

options = Options()
make_UserAgent()
driver = webdriver.Chrome()
driver.get("chrome-extension://hnmpcagpplmpfojmgmnngilcnanddlhb/popup.html")
assert "TestCoper - check Gads" in driver.title
elem = driver.find_element(By.NAME, "q")
elem.clear()
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)
assert "No results found." not in driver.page_source
driver.close()