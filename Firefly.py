import numpy as np 
import matplotlib.pyplot as plt 

#the function that needs to be minimised
#from function import function
def function(X):
   return np.sum(np.square(X),axis=1,keepdims=True)
'''
#hyperparameters
num_feat=int(input("Enter the number of co-ordinates each point has:"))
num_units=int(input("Enter the number of points:"))
c1=float(input("Enter attractiveness coefficient:"))
c2=float(input("Enter light absorbing coefficient:"))
n=int(input("Enter the number of times it will run:"))
'''
num_feat=2
num_units=100
c1=2
c2=3
n=100
def findit(X,Y):
    #return (Y-X)*np.exp(-c2*np.dot((X-Y).T,(X-Y)))
    return (Y-X)*1./(1+c2*np.dot((X-Y).T,(X-Y)))
#initialisation
position=np.random.random((num_units,num_feat))
intensity=function(position)

best_position=(position[np.argmin(intensity)]).reshape(1,num_feat)
for k in range(n):
    for i in range(num_units):
            for j in range(num_units):
                if(intensity[i]<intensity[j]):
                        X=position[i]
                        Y=position[j]
                        position[j]=position[j]+ c1*(X-Y)*1./(1+c2*np.dot((X-Y).T,(X-Y)))+np.random.random((1,num_feat))*(best_position)
                        intensity[j] = function(np.array([position[j]]))
            #just for this
    best_position=(position[np.argmin(intensity)]).reshape(1,num_feat)
    
    plt.scatter(position[:,0],position[:,1])
    plt.pause(1)
    if(k%10==0):
        plt.clf()

            