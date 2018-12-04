
import numpy as np
import matplotlib.pyplot as plt

#the function that needs to be minimised

def function(X):
   return np.sum(np.square(X-2),axis=1,keepdims=True)


#hyperparameters
num_feat=int(input("Enter the number of co-ordinates each point has:"))
num_units=int(input("Enter the number of points:"))
c1=float(input("Enter positional dependence:"))
c2=float(input("Enter global dependence:"))
n=int(input("Enter the number of times it will run:"))

#initialisation
count11=0
position=np.random.random((num_units,num_feat))
'''

#Allows the numbers to start from a specific range
for i in range(num_feat):
    a=float(input("Enter the maximum value "+str(i+1) +" point can have:"))
    b=float(input("Enter the minimum value "+str(i+1) +" point can have:"))
    position[:,i]=position[:,i]*(a-b)+b
'''
best_individual=np.copy(position)
best_pos=position[np.argmin(function(best_individual)),:].reshape(1,num_feat)
velocity=np.random.random((num_units,num_feat))
valuesnow=function(position)
indibestnow=np.copy(valuesnow)
#Iteration to reach the stable point
for i in range(n):
    r1=np.random.random()
    r2=np.random.random()
    velocity= r1*velocity-c1*r1*(position-best_individual)-c2*r2*(position-best_pos)
    position=position+velocity
    valuesnow=function(position)
    temp=(valuesnow<indibestnow)
    temp=temp.reshape(num_units,1)#for the eggholder
    best_individual=best_individual+temp*(position-best_individual)
    indibestnow=indibestnow+temp*(valuesnow-indibestnow)
    best_pos=best_individual[np.argmin(function(best_individual)),:].reshape(1,num_feat)
    #If it reaches a stable point which is not the maxima, it will cause an unequilibruim
    if(np.isclose(np.max(valuesnow),np.min(valuesnow),rtol=1e-4,atol=1e-8)):
        velocity=np.random.random((num_units,num_feat))*best_pos
        count11 +=1
    #Getting a visual for how particles move for two dimensions
    #valuesnow=function(position)
    plt.scatter(position[:,0],position[:,1])
    plt.pause(1)
    if(i%10==0):
        plt.clf()