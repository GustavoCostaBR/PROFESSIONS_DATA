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
import sys

conn = sqlite3.connect('content.sqlite')
conn.execute('PRAGMA foreign_keys = ON')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS Jobs (id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT UNIQUE, link TEXT UNIQUE, Profession TEXT UNIQUE, Workforce TEXT, [Average Age] REAL, [Average Salary] REAL, [Average Male Salary] REAL, [Average Female Salary] REAL, [Total of Male Workers] REAL, [Total of Female Workers] REAL, [Profession Tier] TEXT)')

cur.execute('CREATE TABLE IF NOT EXISTS Vari (Jobs_id INTEGER UNIQUE, vari FLOAT, dev FLOAT, [vari acumul] FLOAT, [disparidade salarial] FLOAT, [disparidade salarial relacao media] FLOAT, [disparidade salarial relacao media cumulativa] FLOAT, FOREIGN KEY(Jobs_id) REFERENCES Jobs(id))')

salario=r"^\$+[+-]?([0-9]*[,])?[0-9]"
milhao=r"^\d+\.\d+M$"
milhar=r"[+-]?([0-9]*[.])?[0-9]+k$"
c=0.0
d=0.0
fs = 0.0
ms = 0.0
diferenca = 0.0
difcumul = 0.0
dispsalrelmed = 0.0
dispsalrelmedcumul = 0.0
somatdisp = 0.0
cur.execute('SELECT MAX(id) FROM Jobs')
max_id = cur.fetchone()[0]

#calculando a media dos salarios e das disparidades salariais entre sexos
for contador in range(1, max_id+1):
	a=0.0
	b=0.0
	cur.execute('SELECT [Workforce] FROM Jobs WHERE id=?', (contador,))
	result = cur.fetchone()

	try:
		if result[0] is None:
			continue
		elif re.match(milhao, result[0]):
			numero = re.findall(r"[0-9.0-9]*", result[0])
			a = (float(numero[0])*1000000)
		elif re.match(milhar, result[0]):
			numero = re.findall(r"[0-9.0-9]*", result[0])
			a = (float(numero[0])*1000)
	except:
		if result is None:
			continue

	cur.execute('SELECT [Average Salary] FROM Jobs WHERE id=?', (contador,))
	result = cur.fetchone()

	if re.match(salario, result[0]):
		numero1 = re.findall(r"[0-9,0-9]*", result[0])
		numero = numero1[1].replace(",", ".")
		b = (float(numero)*1000)
	c=a*b+c
	d=a+d

	cur.execute('SELECT [Average Male Salary] FROM Jobs WHERE id=?', (contador,))
	result = cur.fetchone()
	if result[0] is None:
		continue
	else:
		numero1 = re.findall(r"[0-9,0-9]*", result[0])
		numero = numero1[1].replace(",", ".")
		ms = (float(numero)*1000)
	cur.execute('SELECT [Average Female Salary] FROM Jobs WHERE id=?', (contador,))
	result = cur.fetchone()
	numero1 = re.findall(r"[0-9,0-9]*", result[0])
	numero = numero1[1].replace(",", ".")
	fs = (float(numero)*1000)
	# if fs > ms:
		# print("Isso eh estranho", contador)
	diferenca = ((abs(fs-ms))/fs)
	cur.execute('UPDATE Vari SET ([disparidade salarial]) = (?) WHERE Jobs_id = ?', (diferenca, contador, ))
	difcumul = (diferenca * a) + difcumul
meddifsal = difcumul / d
avg = c/d
# print(avg)
# print(meddifsal)

# prenchendo a tabela das variancias e disparidade com relacao a media
somatvariacumul = 0.0
contador2 = 0.0
contador3 = 0.0
for contador in range(1, max_id+1):
	cur.execute('SELECT Workforce FROM Jobs WHERE id=?', (contador,))
	result = cur.fetchone()
	# print(contador)
	try:
		if result[0] is None:
			cur.execute('INSERT OR IGNORE INTO Vari (Jobs_id) VALUES (?)', (contador, ))
		elif re.match(milhao, result[0]):
			numero = re.findall(r"[0-9.0-9]*", result[0])
			a = (float(numero[0])*1000000)
			contador2 = contador2 + a
			cur.execute('SELECT [Average Salary] FROM Jobs WHERE id=?', (contador, ))
			result = cur.fetchone()
			numero1 = re.findall(r"[0-9,0-9]*", result[0])
			numero = numero1[1].replace(",", ".")
			b = (float(numero)*1000)
			# print("ok1")
			dev = abs(b-avg)
			vari = dev ** 2
			variacumul = a * vari
			somatvariacumul = somatvariacumul + variacumul
			# print("ok1,1")
			cur.execute('INSERT OR IGNORE INTO Vari (Jobs_id) VALUES (?)', (contador, ))
			# print("ok1,2")
			cur.execute('UPDATE Vari SET (vari, dev, [vari acumul]) = (?, ?, ?) WHERE Jobs_id = ?', (vari, dev, variacumul, contador, ))
			# print("ok1,3")
		elif re.match(milhar, result[0]):
			numero = re.findall(r"[0-9.0-9]*", result[0])
			a = (float(numero[0])*1000)
			contador2 = contador2 + a
			cur.execute('SELECT [Average Salary] FROM Jobs WHERE id=?', (contador, ))
			result = cur.fetchone()
			numero1 = re.findall(r"[0-9,0-9]*", result[0])
			numero = numero1[1].replace(",", ".")
			b = (float(numero)*1000)
			# print("ok2")
			dev = abs(b-avg)
			vari = dev ** 2
			variacumul = a * vari
			somatvariacumul = somatvariacumul + variacumul
			# print("ok2,1")
			cur.execute('INSERT OR IGNORE INTO Vari (Jobs_id) VALUES (?)', (contador, ))
			# print("ok2,2")
			cur.execute('UPDATE Vari SET (vari, dev, [vari acumul]) = (?, ?, ?) WHERE Jobs_id = ?', (vari, dev, variacumul, contador, ))
			# print("ok2,3")
			# cur.execute("INSERT OR IGNORE INTO Vari (Jobs_id, vari, dev, [vari acumul]) VALUES (?, ?, ?, ?)", (contador, vari, dev, variacumul))

		cur.execute('SELECT [disparidade salarial] FROM Vari WHERE Jobs_id=?', (contador, ))
		result = cur.fetchone()
		if result[0] is None:
			continue
		else:
			dispsalrelmed = abs(result[0]-meddifsal)
			dispsalrelmedcumul = (dispsalrelmed ** 2) * a
			somatdisp =  somatdisp + dispsalrelmedcumul
			contador3 = contador3 + a
			cur.execute('UPDATE Vari SET ([disparidade salarial relacao media], [disparidade salarial relacao media cumulativa]) = (?, ?) WHERE Jobs_id = ?', (dispsalrelmed, dispsalrelmedcumul, contador, ))
	except:
		continue
conn.commit()
vardisp = somatdisp/(contador3 - 1)
devpaddisp = vardisp ** (1/2)
# print(devpaddisp)
variancia = somatvariacumul/(contador2 - 1)
devpad = variancia ** (1/2)
# print(devpad)

#Preenchendo a tabela com os tier de cada profissao e tier de disparidade

for contador in range(1, max_id+1):
	cur.execute('SELECT [Workforce] FROM Jobs WHERE id=?', (contador,))
	result = cur.fetchone()
	try:
		if result[0] is None:
			cur.execute('UPDATE Jobs SET ([Profession Tier]) = (?) WHERE id = ?', ("Nao listada", contador, ))
		elif re.match(milhao, result[0]):
			cur.execute('SELECT [Average Salary] FROM Jobs WHERE id=?', (contador, ))
			result = cur.fetchone()
			numero1 = re.findall(r"[0-9,0-9]*", result[0])
			numero = numero1[1].replace(",", ".")
			b = (float(numero)*1000)
			if b < (avg - devpad):
				cur.execute('UPDATE Jobs SET ([Profession Tier]) = (?) WHERE id = ?', ("C-", contador, ))
			elif b > (avg - (devpad)) and b < avg:
				cur.execute('UPDATE Jobs SET ([Profession Tier]) = (?) WHERE id = ?', ("C+", contador, ))
			elif b > (avg) and b < (avg+devpad):
				cur.execute('UPDATE Jobs SET ([Profession Tier]) = (?) WHERE id = ?', ("B-", contador, ))
			elif b > (avg+devpad) and b < (avg+2*devpad):
				cur.execute('UPDATE Jobs SET ([Profession Tier]) = (?) WHERE id = ?', ("B+", contador, ))
			elif b > (avg+2*devpad) and b < (avg+3*devpad):
				cur.execute('UPDATE Jobs SET ([Profession Tier]) = (?) WHERE id = ?', ("A-", contador, ))
			else:
				cur.execute('UPDATE Jobs SET ([Profession Tier]) = (?) WHERE id = ?', ("A+", contador, ))
		elif re.match(milhar, result[0]):
			cur.execute('SELECT [Average Salary] FROM Jobs WHERE id=?', (contador, ))
			result = cur.fetchone()
			numero1 = re.findall(r"[0-9,0-9]*", result[0])
			numero = numero1[1].replace(",", ".")
			b = (float(numero)*1000)
			if b < (avg - devpad):
				cur.execute('UPDATE Jobs SET ([Profession Tier]) = (?) WHERE id = ?', ("C-", contador, ))
			elif b > (avg - (devpad)) and b < avg:
				cur.execute('UPDATE Jobs SET ([Profession Tier]) = (?) WHERE id = ?', ("C+", contador, ))
			elif b > (avg) and b < (avg+devpad):
				cur.execute('UPDATE Jobs SET ([Profession Tier]) = (?) WHERE id = ?', ("B-", contador, ))
			elif b > (avg+devpad) and b < (avg+2*devpad):
				cur.execute('UPDATE Jobs SET ([Profession Tier]) = (?) WHERE id = ?', ("B+", contador, ))
			elif b > (avg+2*devpad) and b < (avg+3*devpad):
				cur.execute('UPDATE Jobs SET ([Profession Tier]) = (?) WHERE id = ?', ("A-", contador, ))
			else:
				cur.execute('UPDATE Jobs SET ([Profession Tier]) = (?) WHERE id = ?', ("A+", contador, ))
	except:
		if result is None:
			continue
	cur.execute('SELECT [disparidade salarial] FROM Vari WHERE Jobs_id=?', (contador,))
	result = cur.fetchone()
	if result[0] is None:
		cur.execute('UPDATE Jobs SET ([Salary Disparity]) = (?) WHERE id = ?', ("Nao listada", contador, ))
	elif (result[0]<(meddifsal-(2*devpaddisp))):
		cur.execute('UPDATE Jobs SET ([Salary Disparity]) = (?) WHERE id = ?', ("A+", contador, ))
	elif (result[0]<(meddifsal-(devpaddisp))) and result[0] > (meddifsal-(2*devpaddisp)):
		cur.execute('UPDATE Jobs SET ([Salary Disparity]) = (?) WHERE id = ?', ("A-", contador, ))
	elif (result[0]<(meddifsal)) and result[0] > (meddifsal-(devpaddisp)):
		cur.execute('UPDATE Jobs SET ([Salary Disparity]) = (?) WHERE id = ?', ("B+", contador, ))
	elif (result[0]<(meddifsal+devpaddisp)) and result[0] > (meddifsal):
		cur.execute('UPDATE Jobs SET ([Salary Disparity]) = (?) WHERE id = ?', ("B-", contador, ))
	elif (result[0]<(meddifsal+(2*devpaddisp))) and result[0] > (meddifsal+devpaddisp):
		cur.execute('UPDATE Jobs SET ([Salary Disparity]) = (?) WHERE id = ?', ("C+", contador, ))
	elif (result[0]<(meddifsal+(3*devpaddisp))) and result[0] > (meddifsal+ 2*devpaddisp):
		cur.execute('UPDATE Jobs SET ([Salary Disparity]) = (?) WHERE id = ?', ("C-", contador, ))
	else:
		cur.execute('UPDATE Jobs SET ([Salary Disparity]) = (?) WHERE id = ?', ("D+", contador, ))

conn.commit()

conn.close()

print(f"{avg},{devpad},{meddifsal},{devpaddisp}")