import os
import mraa

def DFDescription():
    df = os.popen("df -h /")
    a = 0
    while True:
        a = a + 1
        line = df.readline()
        if a == 1:
            return(line.split()[0:6])

def DF():
    df = os.popen("df -h /")
    a = 0
    while True:
        a = a + 1
        line = df.readline()
        if a == 2:
            return(line.split()[0:6])

description  = DFDescription()
disk_root = DF()

used_spacea = int(disk_root[4][0])
used_spaceb = int(disk_root[4][1])
used_space = (used_spacea*10) + used_spaceb
unuitlised_space = 100 - used_space

#file logging
with open('disk_util.txt','w') as file:
    file.write('')
with open('disk_util.txt','a') as file:             
                file.write(repr(unutilised_space))
				
				
if(used_space > 0  and used_space < 40):
    print("Utilised Space: "+str(used_space)+ "%")
	print("Unutilised Space: "+str(unutilised_space)+ "%")
	print("OK, Space Available")
	print("\n")
	
elif(used_space > 40 and used_space < 70):
    print("Utilised Space: "+str(used_space)+ "%")
	print("Unutilised Space: "+str(unutilised_space)+ "%")
	print("WARNING: limited Space Available")
	print("\n")

else:
    print("Utilised Space: "+str(used_space)+ "%")
	print("Unutilised Space: "+str(unutilised_space)+ "%")
    print("ERROR: No Space Available")
	print("\n")