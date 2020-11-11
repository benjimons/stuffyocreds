import sys
import os
import glob

mypath = sys.argv[1]
myfiles = []

os.system("mkdir /tmp/stuffyocreds/")
os.system("mkdir /tmp/stuffyocreds/gzips")
os.system("mkdir /tmp/stuffyocreds/toprocess")

for root, dirs, files in os.walk(mypath):
        for file in files:
                myfiles.append(os.path.join(root, file))
        print(len(myfiles))

for x in myfiles:
        os.system("rm -R /tmp/stuffyocreds/gzips/*")
        os.system("rm -R /tmp/stuffyocreds/toprocess/*")

        os.system("cp '"+x+"' /tmp/stuffyocreds/gzips/")
        myfile = glob.glob("/tmp/stuffyocreds/gzips/*")[0]
        os.system("tar xvzf '"+myfile+ "' -C /tmp/stuffyocreds/toprocess/")

        os.system("rm -R /tmp/stuffyocreds/gzips/*")
        
        os.system("python stuffyocreds.py /tmp/stuffyocreds/toprocess")
