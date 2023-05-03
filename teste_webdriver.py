import string
import sqlite3
import urllib.request
from bs4 import BeautifulSoup
import ssl
import var_dump
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from lxml import html
# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


link = 'https://datausa.io/profile/soc/military-specific-occupations'
driver=webdriver.Firefox()
driver.get(link)
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.CLASS_NAME, "stat-value")))

arquivo = (driver.page_source)
#var_dump.var_dump(arquivo)
with open("TesteCod4.txt", "w") as file:
    file.write(arquivo)
driver.quit()


