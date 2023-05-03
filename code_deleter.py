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

cur.execute('SELECT MAX(id) FROM Jobs')
max_id = cur.fetchone()[0]
for contador in range(1, max_id+1):
	conn.commit()
	cur.execute("SELECT content FROM Jobs WHERE id=?", (contador,))
	resultado = cur.fetchone()
	if resultado is not None:
		soup = BeautifulSoup(resultado[0], 'html.parser')
		for tag in soup.find_all('div', {'class': 'profile-subtitle'}):
			conn.commit()
			x = tag.find('p')
			t = x.text
			if t == "Detailed Occupation":
				continue
			if t == "Broad Occupation":
				try:
					cur.execute("DELETE FROM Vari WHERE Jobs_id = ?", (contador,))
					cur.execute("DELETE FROM Jobs WHERE id = ?", (contador,))
				except:
					cur.execute("DELETE FROM Jobs WHERE id = ?", (contador,))
			elif t == "Minor Occupation Group":
				try:
					cur.execute("DELETE FROM Vari WHERE Jobs_id = ?", (contador,))
					cur.execute("DELETE FROM Jobs WHERE id = ?", (contador,))
				except:
					cur.execute("DELETE FROM Jobs WHERE id = ?", (contador,))
			elif t == "Major Occupation Group":
				try:
					cur.execute("DELETE FROM Vari WHERE Jobs_id = ?", (contador,))
					cur.execute("DELETE FROM Jobs WHERE id = ?", (contador,))
				except:
					cur.execute("DELETE FROM Jobs WHERE id = ?", (contador,))
			conn.commit()
	else:
		continue
conn.close()