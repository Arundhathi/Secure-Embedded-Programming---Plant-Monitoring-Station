import os
from subprocess import Popen

#user = "aswami"
#password = "aswami"
#db = "aswami"
#host = "localhost"
#op = "db_backup"

#os.popen("mysqldump -u %s -p%s -h %s -e --opt -c %s | gzip -c > %s.gz"%(user,password,host,db,op)) 

f = open("backup.sql", "w")
x = Popen(["mysqldump","-u","aswami","-paswami","aswami"],stdout = f)
x.wait()
f.close()

