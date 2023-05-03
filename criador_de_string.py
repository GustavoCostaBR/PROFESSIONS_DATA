import re
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
cur.execute('CREATE TABLE IF NOT EXISTS Keywords (id INTEGER PRIMARY KEY AUTOINCREMENT, palavra TEXT UNIQUE, validador INTEGER)')

#print(listacompleta)
cur.execute('SELECT MAX(id) FROM Jobs')
max_id = cur.fetchone()[0]
for contador in range(1, max_id):
	try:

		cur.execute("SELECT link FROM Jobs WHERE id = ?", (contador,))
		resultados=cur.fetchone()[0]
		palavras = re.findall('[a-z]+', resultados)

		for palavra in palavras:
			cur.execute('INSERT OR IGNORE INTO Keywords (palavra, validador) VALUES ( ?, ? )', (palavra, 1) )
	except:
		continue
	conn.commit()
conn.close()