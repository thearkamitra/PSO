#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 17:43:12 2018

@author: arka
"""
file_to_open="/home/arka/Desktop/examples/B5/Praveen Spring '18/B36.log"
def normal_term(file_to_open):
    file=open(file_to_open,'r+')
    X=file.readlines()
    for i in range(len(X)):
        Y=[]
        Y=X[i].split(" ")
        #print(Y)
        if len(Y)>=3 and Y[1]=="Normal":
            if Y[2]=='termination':
                file.close()
                return 1
    
    file.close()
    return 0
def energy(file_to_open,X):
        if(normal_term(file_to_open)==0):
            return X
        file=open(file_to_open,'r+')
        Y=file.readlines()
        for i in range(len(Y)):
            Z=[]
            Z=Y[i].split(" ")
            for j in range(len(Z)):
                if "E(R" in Z[j]:
                    X=Z[j+3]
                    return X
                
