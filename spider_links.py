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
conn.execute('PRAGMA foreign_keys = ON')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS Jobs (id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT UNIQUE, link TEXT UNIQUE, Profession TEXT UNIQUE, Workforce TEXT, [Average Age] REAL, [Average Salary] REAL, [Average Male Salary] REAL, [Average Female Salary] REAL, [Total of Male Workers] REAL, [Total of Female Workers] REAL, [Profession Tier] TEXT)')

cur.execute('CREATE TABLE IF NOT EXISTS Vari (Jobs_id INTEGER UNIQUE, vari FLOAT, dev FLOAT, [vari acumul] FLOAT, [disparidade salarial] FLOAT, [disparidade salarial relacao media] FLOAT, [disparidade salarial relacao media cumulativa] FLOAT, FOREIGN KEY(Jobs_id) REFERENCES Jobs(id))')


cur.execute('SELECT MAX(id) FROM Keywords')
max_id = cur.fetchone()[0]
for contador in range(1, max_id+1):
	conn.commit()
	try:
		cur.execute("SELECT validador FROM Keywords WHERE id = ?", (contador,))
		validador=cur.fetchone()[0]
		cur.execute("SELECT palavra FROM Keywords WHERE id = ?", (contador,))
		palavra=cur.fetchone()[0]
		if validador == 1:
			cur.execute('UPDATE Keywords SET validador = ? WHERE id = ?', (2, contador,))
			try:
				driver = webdriver.Firefox()
				#A definir como funciona o mecanismo quando o site voltar ao ar
				driver.get('https://datausa.io/search/?q='+palavra+'&dimension=PUMS Occupation')

				#parser=html.fromstring(html1)

				wait = WebDriverWait(driver, 2)
				wait.until(EC.presence_of_element_located((By.CLASS_NAME, "result")))
				#print(driver.page_source)
			except:
				print("rodou aqui")
				driver.quit()
				continue
			arquivo = (driver.page_source)
			soup = BeautifulSoup(arquivo, 'lxml')
			body = soup.findAll('li',{'class': 'result'})
			for k,item in enumerate(body):
				x = item.find('a')
				j = x.get('href')
				link = ('https://datausa.io'+ j)
				cur.execute('INSERT OR IGNORE INTO Jobs (link) VALUES ( ? )', (link, ) )
				conn.commit()
			cur.execute('UPDATE Keywords SET validador = ? WHERE id = ?', (2, contador,))
			driver.quit()
		else:
			continue
	except:
		continue
conn.commit()
conn.close()


