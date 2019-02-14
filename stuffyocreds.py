import thread
import time
import threading
import glob
import sys
import os
import mysql.connector

def main(filepath):  
   mydb = mysql.connector.connect(
    host="",
    user="",
    password="",
    database=""
   )

   mycursor = mydb.cursor()

   if not os.path.isfile(filepath):
       print("File path {} does not exist. Exiting...".format(filepath))
       sys.exit()

   bag_of_words = {}
   with open(filepath) as fp:
       print("Starting: "+filepath)
       f = open("/root/credstuffer/log.log", "a")
       f.write(filepath+" started\r\n")
       f.close()
       start = time.time()
       cnt = 0
       for line in fp:
          try:
             cd = line.strip().split(':')
	     if len(cd) <2:
	       cd = line.strip().split(';')
	     val = (cd[0], cd[1], filepath)
             sql = "INSERT INTO creds2 (username, password, filename) VALUES (%s, %s, %s)"
             mycursor.execute(sql, val)
             cnt += 1
             if cnt % 5000 == 0:
		mydb.commit()
      		f = open("/root/credstuffer/log.log", "a")
       		f.write(filepath+" mid processing commit attempt at "+str(cnt)+"\r\n")
	        f.close()
          except mysql.connector.Error as err:
             continue
          except:
             continue
       mydb.commit()
       end = time.time()
       totaltime = end - start
       f = open("/root/credstuffer/log.log", "a")
       f.write(filepath+" in "+str(totaltime)+" added "+str(cnt)+"\r\n")
       f.close()
       print(filepath, " took ", totaltime, " inserted ", cnt)


if __name__ == '__main__':  
   mypath = sys.argv[1]  
   myfiles = []
   for root, dirs, files in os.walk(mypath):
    for file in files:
        myfiles.append(os.path.join(root, file))
   print(len(myfiles))

   for x in myfiles:
      if threading.activeCount() < 20:
	t1 = threading.Thread(target=main,args=(x,))
	t1.start()
      while threading.activeCount() > 19:
        btc=1
