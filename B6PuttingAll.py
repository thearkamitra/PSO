import threading
import numpy as np
import time
import os
import os.path
coordinates=[]
energies=[]

strnames=[]
charge=0
spin=1
molname="B"
#the function that needs to be minimised
def normal_term(file_to_open):
    file=open(file_to_open,'r+')
    X=file.readlines()
    for i in range(len(X)):
        Y=[]
        Y=X[i].split(" ")
        if len(Y)>=3 and Y[2]=="termination":
            if Y[1]=='Normal':
                file.close()
                return 1
            elif Y[1]=="Error":
                file.close()
                return 2
    
    file.close()
    return 0
def energy(name,X,partnum):
        file_to_open=name[:-3]+"log"
        if(normal_term(file_to_open)==2):
            return X
        file=open(file_to_open,'r+')
        Y=file.readlines()
        for i in range(len(Y)):
            Z=[]
            Z=Y[i].split(" ")
            for j in range(len(Z)):
                if "E(" in Z[j]:
                    X=Z[j+3]
                    file.close()
		    lock.acquire()
                    coordinates.append(position[partnum].copy())
                    energies.append(X)
                    strnames.append(file_to_open)
		    lock.release()
                    return X
        file.close()



def gjfconvert(X,iternum,partnum):
    molname="B"
    name="str"+str(partnum)+"_"+str(iternum)+".gjf"
    file=open(name,"w+")
    file.write("%nprocshared=2\n")
    file.write("%mem=2GB\n")
    file.write("%nosave\n")
    file.write("# b3lyp/6-311+g*\n\n")
    file.write("B6 struct\n\n")
    file.write(str(charge)+" "+str(spin)+"\n")
    for i in range(int(len(X)/3)):
        string=" "+molname+"\t\t\t\t\t"+str(round(X[i*3],8))+"\t"+str(round(X[i*3+1],8))+"\t"+str(round(X[i*3+2],8))+"\n"
        file.write(string)
        
    file.write("\n\n\n\n")
    file.close()
    return name

def function(position,iternum,partnum):
        name=gjfconvert(position,iternum,partnum)
        os.system("g09 "+name+" &")
        #time.sleep(3)
        while (os.path.isfile(name[:-3]+"log")) is False:
           pass
        while normal_term(name[:-3]+"log")==0: 
            pass
        valuesnow[i]=energy(name,valuesnow[i],partnum)

#hyperparameters
'''
num_feat=int(input("Enter the number of particles each cluster has:"))
num_units=int(input("Enter the number of particle clusters:"))
c1=float(input("Enter positional dependence:"))
c2=float(input("Enter global dependence:"))
n=int(input("Enter the number of times it will run:"))
'''
num_feat=6
num_units=15
c1=2
c2=2
n=200
Wmax=0.8
Wmin=0.4
num_feat=3*num_feat
#initialisation
position=np.random.random((num_units,num_feat))*6-3
if(os.path.isfile("PresentValuesB6.txt")):
    position=position.reshape((-1,))
    file=open("PresentValuesB6.txt",'r+')
    count=0
    X=file.readlines()
    for i in range(len(X)):
        X[i]=X[i][:-1]
        Y=X[i].split("\t")
        for j in range(len(Y)):
            try:
                position[count]=float(Y[j])
                count +=1
            except:
                pass
    position=position.reshape((num_units,num_feat))
    file.close()
best_individual=np.copy(position)
velocity=np.random.random((num_units,num_feat))
valuesnow=np.zeros((num_units,1),dtype=float)
t=[]
lock=threading.Lock()
for i in range(num_units):
    t.append(threading.Thread(target=function,args=(position[i],0,i)))
for i in range(num_units):
    t[i].start()
for i in range(num_units):
    t[i].join()
best_pos=position[np.argmin(valuesnow),:].reshape(1,num_feat)
temp=np.zeros((num_units,1),dtype=int)
indibestnow=np.copy(valuesnow)

'''for i in range(int(num_units):
    os.remove("str"+str(i)+"_"+str(0)+".gjf")
    os.remove("str"+str(i)+"_"+str(0)+".log")'''
#Iteration to reach the stable point

foldertosave="valuesB6_"
u=0
while(os.path.exists(foldertosave+str(u))):
    u =u+1
os.mkdir(foldertosave+str(u))
foldertosave="valuesB6_"+str(u)

for k in range(1,n):
    r1=np.random.random()
    r2=np.random.random()
    r3=np.random.random()
    w=(Wmax+(Wmin-Wmax)*i/n)
    velocity= w*velocity-c1*r1*(position-best_individual)-c2*r1*(position-best_pos)
    position=position+velocity
    #sleep(200)
    t=[]
    for i in range(num_units):
        t.append(threading.Thread(target=function,args=(position[i],k,i)))
    for i in range(num_units):
        t[i].start()
    for i in range(num_units):
        t[i].join()
    for j in range(num_units):
        if (valuesnow[j]<indibestnow[j]):
            temp[j]=1
        else:
            temp[j]=0
    
    temp=temp.reshape(num_units,1)#for the eggholder
    best_individual=best_individual+temp*(position-best_individual)
    indibestnow=indibestnow+temp*(valuesnow-indibestnow)
    best_pos=best_individual[np.argmin(indibestnow),:].reshape(1,num_feat)
    print("Iteration "+str(k)+" complete at "+time.ctime(time.time()))
    
    
    for i in range(len(energies)):
        for j in range(len(energies)-1):
            if (energies[j+1]>energies[j]):
                energies[j+1],energies[j]=energies[j],energies[j+1]
                coordinates[j+1],coordinates[j]=coordinates[j],coordinates[j+1]
                strnames[j+1],strnames[j]=strnames[j],strnames[j+1]

    print("--------------------------------")
    print (len(energies))
    f=open(foldertosave+"/all_valuesB6_"+str(int(k/50))+".txt",'w+')
    for i in range(len(energies)):
        f.write("\n\n"+str(strnames[i])+"\n")
        f.write(str(energies[i])+"\n\n")
        for j in range(int(num_feat/3)):
            f.write(" "+molname+"\t\t\t\t\t"+str(coordinates[i][j*3])+"\t"+str(coordinates[i][j*3+1])+"\t"+str(coordinates[i][j*3+2])+"\t\n")
    f.close()
    
    for i in range(int(num_units)):
    	os.remove("str"+str(i)+"_"+str(k-1)+".gjf")
    	os.remove("str"+str(i)+"_"+str(k-1)+".log")

	