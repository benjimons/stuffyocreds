import thread
import time
import datetime
import threading
import glob
import sys
import os
import mysql.connector
import logging


def main(filepath):  
	mydb = mysql.connector.connect(
		host="127.0.0.1",
		user="root",
		password="root",
		database="credstuffer"
	)

	mycursor = mydb.cursor()
	mycursor2 = mydb.cursor()
	
	if not os.path.isfile(filepath):
		logging.error("File path {} does not exist. Exiting...".format(filepath))
		sys.exit()

	bag_of_words = {}
	logging.debug(filepath+" opening")
	with open(filepath) as fp:
		start = time.time()
		cnt = 0
		find = False 
		for line in fp:
			try:
				cd = line.strip().split(':')
				
				if len(cd) <2:
					cd = line.strip().split(';')
				
				val = (cd[0], cd[1], filepath)
					
				if cnt==0:
					checksql = "SELECT * FROM creds2 WHERE username=%s AND password=%s AND filename=%s LIMIT 1";
					mycursor2.execute(checksql, val)
					row=mycursor2.fetchone()
					if row is not None:
						logging.debug(filepath+" is already indexed, skipping "+str(row[0]))
						find = True
						break
					else:
						logging.debug(filepath+" appears new, continuing")
						
				sql = "INSERT INTO creds2 (username, password, filename) VALUES (%s, %s, %s)"
				mycursor.execute(sql, val)
				cnt += 1
				if cnt % 5000 == 0:
					mydb.commit()
					logging.debug(filepath+" mid processing commit attempt at "+str(cnt))
						
			except mysql.connector.Error as err:
				logging.error(str(err))
				continue
			except IndexError as err:
				continue
			except Exception as err:
				logging.error(filepath+" "+str(err))
				continue
				
		if find: 
			return
		#Final commit before finishing the file
		mydb.commit()
		end = time.time()
		totaltime = end - start
		logging.info(filepath+" finished in "+str(totaltime)+" added "+str(cnt))

if __name__ == '__main__':  
	#Set up the logging
	logfile = "logger.log"
	logging.basicConfig(level=logging.DEBUG, filename=logfile, format='%(asctime)s %(levelname)s %(name)s %(message)s')
	
	mypath = sys.argv[1]  
	myfiles = []
	for root, dirs, files in os.walk(mypath):
		for file in files:
			myfiles.append(os.path.join(root, file))
	print(len(myfiles))


	for x in myfiles:
		if threading.activeCount() < 2:
			t1 = threading.Thread(target=main,args=(x,))
			logging.debug("Spinning new thread to sniff file: "+x)
			t1.start()
		while threading.activeCount() > 1:
			btc=1
