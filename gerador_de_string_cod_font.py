import re
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

arquivo = open('TesteCod.txt', 'r')
conteudo = arquivo.read()
palavras = re.findall ('"Detailed Occupation":"(.+?)"', conteudo)


for palavra in palavras:
	palavras2 = re.findall('[a-zA-Z]+', palavra)
	for palavra2 in palavras2:
		palavra3 = palavra2.lower()
		cur.execute('INSERT OR IGNORE INTO Keywords (palavra, validador) VALUES ( ?, ? )', (palavra3, 1) )

conn.commit()
conn.close()
arquivo.close()