import sqlite3
import re
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt2
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
avg = float(sys.argv[1])
devpad = float(sys.argv[2])
devpaddisp = float(sys.argv[4])
meddifsal = float(sys.argv[3])

p1 = p2 = p3 = p4 = p5 = p6 = a1 = a2 = a3 = a4 =a5 = a6 = pd1 = pd2 = pd3 = pd4 = pd5 = pd6 = ad1 = ad2 = ad3 = ad4 = ad5 = ad6 = ad = pd = 0.0

cur.execute('SELECT MAX(id) FROM Jobs')
max_id = cur.fetchone()[0]

for contador in range(1, max_id+1):
	cur.execute('SELECT [Profession Tier] FROM Jobs WHERE id=?', (contador,))
	result = cur.fetchone()
	cur.execute('SELECT Workforce FROM Jobs WHERE id=?', (contador,))
	result1 = cur.fetchone()
	if result == None:
		continue
	elif result[0] == "Nao listada":
		continue
	elif result[0] == "C-":
		a1 = a1 +1
		if re.match(milhao, result1[0]):
			numero = re.findall(r"[0-9.0-9]*", result1[0])
			a = (float(numero[0])*1000000)
			p1 = p1 + a
		else :
			numero = re.findall(r"[0-9.0-9]*", result1[0])
			a = (float(numero[0])*1000)
			p1 = p1 + a
	elif result[0] == "C+":
		a2 = a2 +1
		if re.match(milhao, result1[0]):
			numero = re.findall(r"[0-9.0-9]*", result1[0])
			a = (float(numero[0])*1000000)
			p2 = p2 + a
		else :
			numero = re.findall(r"[0-9.0-9]*", result1[0])
			a = (float(numero[0])*1000)
			p2 = p2 + a
	elif result[0] == "B-":
		a3 = a3 +1
		if re.match(milhao, result1[0]):
			numero = re.findall(r"[0-9.0-9]*", result1[0])
			a = (float(numero[0])*1000000)
			p3 = p3 + a
		else :
			numero = re.findall(r"[0-9.0-9]*", result1[0])
			a = (float(numero[0])*1000)
			p3 = p3 + a
	elif result[0] == "B+":
		a4 = a4 +1
		if re.match(milhao, result1[0]):
			numero = re.findall(r"[0-9.0-9]*", result1[0])
			a = (float(numero[0])*1000000)
			p4 = p4 + a
		else :
			numero = re.findall(r"[0-9.0-9]*", result1[0])
			a = (float(numero[0])*1000)
			p4 = p4 + a
	elif result[0] == "A-":
		a5 = a5 +1
		if re.match(milhao, result1[0]):
			numero = re.findall(r"[0-9.0-9]*", result1[0])
			a = (float(numero[0])*1000000)
			p5 = p5 + a
		else :
			numero = re.findall(r"[0-9.0-9]*", result1[0])
			a = (float(numero[0])*1000)
			p5 = p5 + a
	else:
		a6 = a6 +1
		if re.match(milhao, result1[0]):
			numero = re.findall(r"[0-9.0-9]*", result1[0])
			a = (float(numero[0])*1000000)
			p6 = p6 + a
		else :
			numero = re.findall(r"[0-9.0-9]*", result1[0])
			a = (float(numero[0])*1000)
			p6 = p6 + a

	cur.execute('SELECT [Salary Disparity] FROM Jobs WHERE id=?', (contador,))
	result = cur.fetchone()
	if result[0] == "Nao listada":
		continue
	elif result[0] == "D+":
		ad = ad +1
		if re.match(milhao, result1[0]):
			numero = re.findall(r"[0-9.0-9]*", result1[0])
			a = (float(numero[0])*1000000)
			pd = pd + a
		else :
			numero = re.findall(r"[0-9.0-9]*", result1[0])
			a = (float(numero[0])*1000)
			pd = pd + a
	elif result[0] == "C-":
		ad1 = ad1 +1
		if re.match(milhao, result1[0]):
			numero = re.findall(r"[0-9.0-9]*", result1[0])
			a = (float(numero[0])*1000000)
			pd1 = pd1 + a
		else :
			numero = re.findall(r"[0-9.0-9]*", result1[0])
			a = (float(numero[0])*1000)
			pd1 = pd1 + a
	elif result[0] == "C+":
		ad2 = ad2 +1
		if re.match(milhao, result1[0]):
			numero = re.findall(r"[0-9.0-9]*", result1[0])
			a = (float(numero[0])*1000000)
			pd2 = pd2 + a
		else :
			numero = re.findall(r"[0-9.0-9]*", result1[0])
			a = (float(numero[0])*1000)
			pd2 = pd2 + a
	elif result[0] == "B-":
		ad3 = ad3 +1
		if re.match(milhao, result1[0]):
			numero = re.findall(r"[0-9.0-9]*", result1[0])
			a = (float(numero[0])*1000000)
			pd3 = pd3 + a
		else :
			numero = re.findall(r"[0-9.0-9]*", result1[0])
			a = (float(numero[0])*1000)
			pd3 = pd3 + a
	elif result[0] == "B+":
		ad4 = ad4 +1
		if re.match(milhao, result1[0]):
			numero = re.findall(r"[0-9.0-9]*", result1[0])
			a = (float(numero[0])*1000000)
			pd4 = pd4 + a
		else :
			numero = re.findall(r"[0-9.0-9]*", result1[0])
			a = (float(numero[0])*1000)
			pd4 = pd4 + a
	elif result[0] == "A-":
		ad5 = ad5 +1
		if re.match(milhao, result1[0]):
			numero = re.findall(r"[0-9.0-9]*", result1[0])
			a = (float(numero[0])*1000000)
			pd5 = pd5 + a
		else :
			numero = re.findall(r"[0-9.0-9]*", result1[0])
			a = (float(numero[0])*1000)
			pd5 = pd5 + a
	else:
		ad6 = ad6 +1
		if re.match(milhao, result1[0]):
			numero = re.findall(r"[0-9.0-9]*", result1[0])
			a = (float(numero[0])*1000000)
			pd6 = pd6 + a
		else :
			numero = re.findall(r"[0-9.0-9]*", result1[0])
			a = (float(numero[0])*1000)
			pd6 = pd6 + a


# data for the bars
x1 = ["C-\n" + "Less than\n$" + str(round(((avg - devpad)), 2)), "C+\n" + "$" + str(round(((2 * avg - devpad)/2), 2)), "B-\n" + "$" + str(round(((2 * avg + devpad)/2), 2)), "B+\n" + "$" + str(round(((2 * avg + 3 * devpad)/2), 2)), "A-\n" + "$" + str(round(((2 * avg + 5 * devpad)/2), 2)), "A+\n" + "More than\n$" + str(round(((avg + 3 * devpad)), 2))]

x2 = ["D+\n" + "Fraction of disparity\nMore than " + str(round(((meddifsal + 3 * devpaddisp)), 2)),"C-\n" + "Fraction of disparity\n" + str(round(((2*meddifsal + 5 * devpaddisp)/2), 2)), "C+\n" + "Fraction of disparity\n" + str(round(((2 * meddifsal + 3 *devpaddisp)/2), 2)), "B-\n" + "Fraction of disparity\n" + str(round(((2 * meddifsal + devpaddisp)/2), 2)), "B+\n" + "Fraction of disparity\n" + str(round(((2 * meddifsal - devpaddisp)/2), 2)), "A-\n" + "Fraction of disparity\n" + str(round(((2 * meddifsal - 3 * devpaddisp)/2), 2))]
yt1 = [a1, a2, a3, a4, a5, a6]
yt2 = [p1, p2, p3, p4, p5, p6]
yt3 = [ad, ad1, ad2, ad3, ad4, ad5]
yt4 = [pd, pd1, pd2, pd3, pd4, pd5]

# create the bar chart
plt.bar(x1, yt1)

# set the chart title and axis labels
plt.title("Salaries x Professions")
plt.xlabel("Category of salary")
plt.ylabel("Number of professions")

# display the chart
plt.show()

# create the bar chart
plt2.bar(x2, yt3)

# set the chart title and axis labels
plt2.title("Gender Disparity x Professions")
plt2.xlabel("Category of gender disparity")
plt2.ylabel("Number of professions")

# display the chart
plt2.show()


# create the bar chart
plt.bar(x1, yt2)

# set the chart title and axis labels
plt.title("Salaries x People employed")
plt.xlabel("Category of salary")
plt.ylabel("Number of workers")

# display the chart
plt.show()


# create the bar chart
plt2.bar(x2, yt4)

# set the chart title and axis labels
plt2.title("Gender Disparity x People employed")
plt2.xlabel("Category of gender disparity")
plt2.ylabel("Number of workers")

# display the chart
plt2.show()





conn.close()
quit()