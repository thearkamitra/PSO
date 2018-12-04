import numpy as np
molname="B"
spin=1
def gjfconvert(X,iternum,partnum):
    name="str"+str(partnum)+"_"+str(iternum)+".gjf"
    file=open(name,"w+")
    file.write("%nprocshared=4\n")
    file.write("%mem=8GB\n")
    file.write("%nosave\n")
    file.write("# b3lyp/6-311+g*\n\n")
    file.write("B6 struct\n\n")
    if spin==1:
        file.write("0 1\n")
        #print("HAha")
    else:
        file.write("0 3\n")
    for i in range(int(len(X)/3)):
        string=" "+molname+"\t\t\t\t\t"+str(X[i*3])+"\t"+str(X[i*3+1])+"\t"+str(X[i*3+2])+"\n"
        file.write(string)
        
    file.write("\n\n\n\n")
    file.close()
    return 
        
X=[1,2,3]
iternum=4
partnum=2
gjfconvert(X,iternum,partnum)
