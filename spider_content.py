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


conn = sqlite3.connect('content.sqlite')
cur = conn.cursor()

cur.execute("SELECT MAX(id) FROM Jobs")
max_id = int(cur.fetchone()[0])
for id in range(1,max_id+1):
	try:
		cur.execute("SELECT link FROM Jobs WHERE id = ?", (id,))
		link = cur.fetchone()[0]
		cur.execute("SELECT content FROM Jobs WHERE id = ?", (id,))
		content = cur.fetchone()[0]
		if content is not None:
			continue
	except:
		continue
	try:
		driver=webdriver.Firefox()
		driver.get(link)
		wait = WebDriverWait(driver, 0)
		wait.until(EC.presence_of_element_located((By.CLASS_NAME, "profile-stats")))
	except:
		driver.quit()
		continue
	arquivo = (driver.page_source)
	# var_dump.var_dump(arquivo)
	cur.execute('UPDATE Jobs SET content = ? WHERE id = ?', (arquivo, id,))
	driver.quit()
	conn.commit()

conn.close()



