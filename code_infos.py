import string
import sqlite3
import urllib.request
from bs4 import BeautifulSoup
import ssl
import re
import var_dump
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


conn = sqlite3.connect('content.sqlite')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS Jobs (id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT UNIQUE, link TEXT UNIQUE, Profession TEXT UNIQUE, Workforce TEXT, [Average Age] REAL, [Average Salary] REAL, [Average Male Salary] REAL, [Average Female Salary] REAL, [Total of Male Workers] REAL, [Total of Female Workers] REAL)')


work = '([0-9]+ Workforce)'
cur.execute('SELECT MAX(id) FROM Jobs')
max_id = cur.fetchone()[0]
for contador in range(1, max_id+1):
	conn.commit()
	try:
		cur.execute("SELECT link FROM Jobs WHERE id=?", (contador,))
		result = cur.fetchone()
		profi = re.findall(r"soc/(.+)", result[0])
		profireal = profi[0].replace("-", " ")
		cur.execute("UPDATE Jobs SET Profession = ? WHERE id = ?", (profireal, contador))
	except:
		continue
	cur.execute("SELECT content FROM Jobs WHERE id=?", (contador,))
	resultado = cur.fetchone()
	soup = BeautifulSoup(resultado[0], 'html.parser')
	a=1
	for tag in soup.find_all('div', {'class': 'stat-title'}):
		if re.match(work, tag.text) and a==1:
			try:
				next_tag = tag.find_next_sibling('div').text
				cur.execute("UPDATE Jobs SET Workforce = ? WHERE id = ?", (next_tag, contador))
				a=2
			except:
				continue
		elif re.match("Average Age", tag.text):
			try:
				next_tag = tag.find_next_sibling('div').text
				cur.execute("UPDATE Jobs SET [Average Age] = ? WHERE id = ?", (next_tag, contador))
			except:
				continue
		elif re.match("Average Salary", tag.text):
			try:
				next_tag = tag.find_next_sibling('div').text
				cur.execute("UPDATE Jobs SET [Average Salary] = ? WHERE id = ?", (next_tag, contador))
			except:
				continue
		elif re.match("Average Male Salary", tag.text):
			try:
				next_tag = tag.find_next_sibling('div').text
				cur.execute("UPDATE Jobs SET [Average Male Salary] = ? WHERE id = ?", (next_tag, contador))
			except:
				continue
		elif re.match("Average Female Salary", tag.text):
			try:
				next_tag = tag.find_next_sibling('div').text
				cur.execute("UPDATE Jobs SET [Average Female Salary] = ? WHERE id = ?", (next_tag, contador))
			except:
				continue
		elif re.match("MALE WORKFORCE", tag.text):
			try:
				previous_tag = tag.find_previous_sibling('div').text
				cur.execute("UPDATE Jobs SET [Total of Male Workers] = ? WHERE id = ?", (previous_tag, contador))
			except:
				continue
		elif re.match("FEMALE WORKFORCE", tag.text):
			try:
				previous_tag = tag.find_previous_sibling('div').text
				cur.execute("UPDATE Jobs SET [Total of Female Workers] = ? WHERE id = ?", (previous_tag, contador))
				conn.commit()
				break
			except:
				continue
		conn.commit()

conn.close()