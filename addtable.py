import sqlite3

# connect to the database
conn = sqlite3.connect('content.sqlite')
c = conn.cursor()

# add column(s) to the table

# c.execute("ALTER TABLE Jobs ADD COLUMN Profession TEXT")
# c.execute("ALTER TABLE Jobs ADD COLUMN Workforce TEXT")
# c.execute("ALTER TABLE Jobs ADD COLUMN [Average Age] REAL")
# c.execute("ALTER TABLE Jobs ADD COLUMN [Average Salary] REAL")
# c.execute("ALTER TABLE Jobs ADD COLUMN [Average Male Salary] REAL")
# c.execute("ALTER TABLE Jobs ADD COLUMN [Average Female Salary] REAL")
# c.execute("ALTER TABLE Jobs ADD COLUMN [Total of Male Workers] REAL")
# c.execute("ALTER TABLE Jobs ADD COLUMN [Profession Tier] Text")
# c.execute("ALTER TABLE Vari ADD COLUMN [vari acumul] FLOAT")
# c.execute("ALTER TABLE Vari ADD COLUMN [disparidade salarial] FLOAT")
# c.execute("ALTER TABLE Vari ADD COLUMN [disparidade salarial relacao media] FLOAT")
# c.execute("ALTER TABLE Vari ADD COLUMN [disparidade salarial relacao media cumulativa] FLOAT")
# c.execute("ALTER TABLE Vari ADD CONSTRAINT my_column_unique UNIQUE Jobs_id")

c.execute("ALTER TABLE Jobs ADD COLUMN [Salary Disparity] TEXT")

# c.execute("ALTER TABLE Jobs RENAME COLUMN [Profession Tier] TO [Profession Tier by Salary]")


conn.commit()
conn.close()
