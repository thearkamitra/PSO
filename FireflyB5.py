import threading
import numpy as np
import time
import os
import os.path
coordinates=[]
energies=[]
velocities=[]
strnames=[]
charge=0
spin=2
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
                    velocities.append(velocity[partnum].copy())
                    energies.append(X)
                    valuesnow[partnum]=X
                    strnames.append(file_to_open)
                    lock.release()
                    return X
        file.close()



def gjfconvert(X,iternum,partnum,threadnums):
    molname="B"
    name="str"+str(partnum)+"_"+str(iternum)+".gjf"
    file=open(name,"w+")    
    file.write("%nprocshared="+str(int(30/threadnums))+"\n")
    file.write("%mem=2GB\n")
    file.write("%nosave\n")
    file.write("# b3lyp/6-311+g*\n\n")
    file.write("B5 struct\n\n")
    file.write(str(charge)+" "+str(spin)+"\n")
    for i in range(int(len(X)/3)):
        string=" "+molname+"\t\t\t\t\t"+str(round(X[i*3],8))+"\t"+str(round(X[i*3+1],8))+"\t"+str(round(X[i*3+2],8))+"\n"
        file.write(string)
        
    file.write("\n\n\n\n")
    file.close()
    return name

def function(position,iternum,partnum,threadnums):
        name=gjfconvert(position,iternum,partnum,threadnums)
        os.system("g09 "+name+" &")
        #time.sleep(3)
        while (os.path.isfile(name[:-3]+"log")) is False:
           pass
        while normal_term(name[:-3]+"log")==0: 
            pass
        energy(name,valuesnow[partnum],partnum)
        os.remove(name)
        os.remove(name[:-3]+"log")

#hyperparameters
'''
num_feat=int(input("Enter the number of particles each cluster has:"))
num_units=int(input("Enter the number of particle clusters:"))
c1=float(input("Enter positional dependence:"))
c2=float(input("Enter global dependence:"))
n=int(input("Enter the number of times it will run:"))
'''
num_feat=5
num_units=15
c1=0.2
c2=0.9
a=0.1
p=0.97
n=1000
num_feat=3*num_feat
#initialisation
position=np.random.random((num_units,num_feat))*6-3
velocity=np.random.random((num_units,num_feat))
if(os.path.isfile("PresentValues.txt")):
    position=position.reshape((-1,))
    file=open("PresentValues.txt",'r+')
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
#position=position+0.1*velocity########################################################change
#############################################################################################################################
if(os.path.isfile("PresentValuesVelocity.txt")):
    velocity=velocity.reshape((-1,))
    file=open("PresentValuesVelocity.txt",'r+')
    count=0
    X=file.readlines()
    for i in range(len(X)):
        X[i]=X[i][:-1]
        Y=X[i].split("\t")
        for j in range(len(Y)):
            try:
                velocity[count]=float(Y[j])
                count +=1
            except:
                pass
    velocity=velocity.reshape((num_units,num_feat))
    file.close()

best_individual=np.copy(position)
valuesnow=np.zeros((num_units,1),dtype=float)
t=[]
lock=threading.Lock()
for i in range(num_units):
    t.append(threading.Thread(target=function,args=(position[i],0,i,15)))
    t[i].start()
for i in range(num_units):
    t[i].join()
best_pos=position[np.argmin(valuesnow),:].reshape(1,num_feat)
temp=np.zeros((num_units,1),dtype=int)
indibestnow=np.copy(valuesnow)


foldertosave="valueB5_"
u=0
while(os.path.exists(foldertosave+str(u))):
    u =u+1
os.mkdir(foldertosave+str(u))
foldertosave="valueB5_"+str(u)
'''for i in range(int(num_units):
    os.remove("str"+str(i)+"_"+str(0)+".gjf")
    os.remove("str"+str(i)+"_"+str(0)+".log")'''
#Iteration to reach the stable point
print("Iteration 0 complete at "+time.ctime(time.time()))
print("--------------------------------")
print (len(energies))
k=0
f=open(foldertosave+"/all_values"+str(int(k/50))+".txt",'w+')
init=open(foldertosave+"initialvalues.txt","w")
initvel=open(foldertosave+"initialvel.txt","w")
fi=open(foldertosave+"/all_velocities_"+str(int(k/50))+".txt",'w+')
for i in range(len(energies)):
    f.write("\n\n"+str(strnames[i])+"\n")
    init.write("\n\n"+str(strnames[i])+"\n")
    f.write(str(energies[i])+"\n\n")
    init.write(str(energies[i])+"\n\n")
    for j in range(int(num_feat/3)):
        f.write(" "+molname+"\t\t\t\t\t"+str(coordinates[i][j*3])+"\t"+str(coordinates[i][j*3+1])+"\t"+str(coordinates[i][j*3+2])+"\t\n")
        init.write(" "+molname+"\t\t\t\t\t"+str(coordinates[i][j*3])+"\t"+str(coordinates[i][j*3+1])+"\t"+str(coordinates[i][j*3+2])+"\t\n")
    fi.write("\n\n"+str(strnames[i])+"\n")
    initvel.write("\n\n"+str(strnames[i])+"\n")   
    fi.write(str(energies[i])+"\n\n")
    initvel.write(str(energies[i])+"\n\n")
    for j in range(int(num_feat/3)):
        fi.write(" "+molname+"\t\t\t\t\t"+str(velocities[i][j*3])+"\t"+str(velocities[i][j*3+1])+"\t"+str(velocities[i][j*3+2])+"\t\n")
        initvel.write(" "+molname+"\t\t\t\t\t"+str(velocities[i][j*3])+"\t"+str(velocities[i][j*3+1])+"\t"+str(velocities[i][j*3+2])+"\t\n")
fi.close()
initvel.close()
init.close()
f.close()
for k in range(1,n):
    p=p*0.97
    for i in range(num_units):
        toedit=[]
        for j in range(num_units):
            if(valuesnow[i]<valuesnow[j]):
                position[j]=position[j]-c1*(position[j]-position[i])*(1/(1+c2*((position[j]-position[i]).T*(position[j]-position[i]))))+0.1*p*(np.random.random((1,num_feat))-0.5)
                toedit.append(j)
        t=[]
        for j in range(len(toedit)):
            t.append(threading.Thread(target=function,args=(position[toedit[j]],k,toedit[j],len(toedit))))
            t[j].start()
        for j in range(len(t)):
            t[j].join()

    best_pos=best_individual[np.argmin(indibestnow),:].reshape(1,num_feat)
    print("Iteration "+str(k)+" complete at "+time.ctime(time.time()))
    
    
    for i in range(len(energies)):
        for j in range(len(energies)-1):
            if (energies[j+1]>energies[j]):
                energies[j+1],energies[j]=energies[j],energies[j+1]
                coordinates[j+1],coordinates[j]=coordinates[j],coordinates[j+1]
                strnames[j+1],strnames[j]=strnames[j],strnames[j+1]
                velocities[j+1],velocities[j]=velocities[j],velocities[j+1]

    print("--------------------------------")
    print (len(energies))
    f=open(foldertosave+"/all_values"+str(int(k/50))+".txt",'w+')
    fi=open(foldertosave+"/all_velocities_"+str(int(k/50))+".txt",'w+')
    for i in range(len(energies)):
        f.write("\n\n"+str(strnames[i])+"\n")
        f.write(str(energies[i])+"\n\n")
        for j in range(int(num_feat/3)):
            f.write(" "+molname+"\t\t\t\t\t"+str(coordinates[i][j*3])+"\t"+str(coordinates[i][j*3+1])+"\t"+str(coordinates[i][j*3+2])+"\t\n")
        fi.write("\n\n"+str(strnames[i])+"\n")   
        fi.write(str(energies[i])+"\n\n")
        for j in range(int(num_feat/3)):
            fi.write(" "+molname+"\t\t\t\t\t"+str(velocities[i][j*3])+"\t"+str(velocities[i][j*3+1])+"\t"+str(velocities[i][j*3+2])+"\t\n")
    fi.close()
    f.close()

    