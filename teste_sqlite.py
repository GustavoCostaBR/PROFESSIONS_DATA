import sqlite3

conn = sqlite3.connect('championships.db')

cursor = conn.cursor()
table_names = ['premiere_league_table', 'scottish_premiership_table', 'eng_championship_table']

for index in table_names:
    	# # # select the data from the table with an ordered position column
	cursor.execute(f"SELECT row_number() OVER (ORDER BY pontos DESC, [saldo de gols] DESC, [gols pró] DESC) AS position, [Nome do time], pontos, [saldo de gols] FROM {index}")

	rows = cursor.fetchall()
	for row in rows:
		print(row)

conn.close()