import sqlite3
import os
import pandas as pd


def createHistoricTable(xl_dir):

	conn = sqlite3.connect('historic_data.db')
	print ("Opened database successfully")

	conn.execute('''CREATE TABLE IF NOT EXISTS HISTORIC_AQ
	        (CITY          TEXT     NOT NULL,
	         LOCATION      TEXT     NOT NULL,
	         DATE_TIME     TEXT     NOT NULL,
	         PM10          REAL,
	         CO            REAL,
	         SO2           REAL,
	         NO2           REAL,
	         NOX           REAL,
	         O3            REAL);''')
	print ("Table created successfully")

	BASE_DIR = './veriler/'

	l_attributes = ['PM10 ( µg/m3 )', 'SO2 ( µg/m3 )', 'CO ( µg/m3 )', 'NO2 ( µg/m3 )', 'NOX ( µg/m3 )', 'O3 ( µg/m3 )']

	for xlsx in os.listdir(BASE_DIR):

		df = pd.read_excel(BASE_DIR + xlsx)

		print(BASE_DIR + xlsx)

		t_attributes = []

		for index, row in df.iterrows():
			if index == 0:
				t_attributes = row.tolist()[1:]
				continue
			city = list(row.to_dict().keys())[1].split(' - ')[0]
			location = list(row.to_dict().keys())[1]

			time_str = str(row.tolist()[0])
			zipped_values = list(zip(t_attributes, row.tolist()[1:]))

			corrected_row = []

			for attrib in l_attributes:
				match = False
				for elm in zipped_values:
					if attrib == elm[0]:
						if elm[1] == '-':
							corrected_row.append(-1)
						else:
							corrected_row.append(elm[1])
						match = True

				if not match:
					corrected_row.append(-1)

			db_row = [city, location, time_str]+corrected_row

			conn.execute('insert into HISTORIC_AQ values (?,?,?,?,?,?,?,?,?)', db_row)
			conn.commit()
	conn.close()

	# cur = conn.cursor()
	# cur.execute("SELECT * FROM HISTORIC_AQ")
	# rows = cur.fetchall()
	# for row in rows:
	# 	print(row)

def updateHistoricTable():
	return

def createForcastTable():
	return

def updateForcastTable():
	return

createHistoricTable(".")

# if os.path.exists('./historic_data.db'):
# 	##### TODO: UPDATE the existing database
#	updateHistoricTable()
#	updateForcastTable()

# else:
# 	createHistoricTable("")
#	createForcastTable()

