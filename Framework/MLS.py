import torch
import os
import torch.nn as nn
import numpy as np
import pandas as pd
import statistics
from numpy import genfromtxt
from sklearn.preprocessing import StandardScaler    
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler    
from sklearn import preprocessing
from sklearn.datasets import make_classification
from sklearn.multioutput import MultiOutputClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.utils import shuffle
import numpy as np
import globals
PATH = 'model.pt'

def save_checkpoint(new_score_track, new_model_state_dict, PATH):
 torch.save({'score_track': new_score_track,
 'net_state_dict': new_model_state_dict
 }, PATH)


def MachineLearning(nomeArq, n, DIn, DOut, PATH):

    N, D_in, H, D_out = n, DIn, 10000, DOut
    
    
    training = np.genfromtxt("Calibracao.txt", delimiter=',').astype(float) 

    print(training)
 
    print(D_in)
 
    a =3
    b= 3+D_in   
    X = np.genfromtxt("Calibracao.txt", delimiter=',',usecols=range(a,b)).astype(float) 
      
    print(X)

    a =3+D_in
    b= 3+D_in+D_out
    Y = np.genfromtxt("Calibracao.txt", delimiter=',',usecols=range(a,b)).astype(float) 

    print(Y)


    Y = Y.reshape((-D_out, D_out)).astype(float) 
    
    print(Y)

    n_samples, n_features = X.shape # 10,100
    n_outputs = Y.shape[1]
    n_classes = 3
    
    forest = RandomForestClassifier(random_state=globals.random_state_seed)
    multi_target_forest = MultiOutputClassifier(forest, n_jobs=-1)
    Rgr = multi_target_forest.fit(X, Y)
    
    

    return Rgr
 
#Start loop
 
def ML(Arquivo):
 
    filename = Arquivo
    #'Calibracao.txt'
    dadoE=[]
    
    with open(filename) as f:
        content = f.read().splitlines()
        for line in content:
            contentBreak = line.split(",")
            for temp in contentBreak:
                dadoE.append(temp)
            break    
                
    # print(dadoE)            
    
    DIn = (int)(dadoE[1])
    
    DOut = (int)(dadoE[2])
    
    fileObject = open(filename)
    n = sum(1 for row in fileObject) 
    
    print(n,DIn,DOut)
    
    globals.model = MachineLearning('Calibracao.txt', n, DIn, DOut, PATH)
    
    
    # X = np.array([[30.0,35.0,57.1,50.6,2.0,2.0,15.8,0.52,0.67]])
    # print( globals.model.predict(X))
    
    #X = np.array([[15.0,8.0,22.59,16.94,128.88,13.06,39.71]])#15_8_Se_R_A__0,7,1,15.0,8.0,22.59,16.94,128.88,13.06,39.71,2
    #print("globals.model.predict(X) -> 2")
    #print( globals.model.predict(X))
    