import torch
import os
import torch.nn as nn
import numpy as np
import pandas as pd
import statistics

from importlib.metadata import files
from os import listdir
from os.path import *
from MLS import *

from numpy import genfromtxt
from sklearn.preprocessing import StandardScaler    
from sklearn.model_selection import train_test_split
#from CDC import *
from sklearn.preprocessing import StandardScaler    
from Otimizacao import *
from sklearn import preprocessing
import numpy
from scipy import stats

#import globals

from read import *
   


def ML_Solver(path, arquivoML, arquivoSaida ,tolerance, temp_exec):
    files = listar_arquivos(path)
    files.sort(reverse=True)
    #files.sort()
    
    Lista = []
    Lista.append((0,"BL d_linha"))
    Lista.append((1,"BL p_linha"))
    Lista.append((2,"BL p+d"))
    Lista.append((3,"BL p+d Rest"))

      
    #remover as instancias que já foram executadas da lista
    myfile = open(arquivoSaida,"a+")   #open('Instances.txt')
    next_line = myfile.readline()
    
    while next_line != "" and next_line != "\n": 
       split_line = next_line.split(',')
       inst_exec = split_line[0]
       print("Removendo : ",inst_exec)
       inst_exec = inst_exec + ".txt"
       files.remove(inst_exec)
       next_line = myfile.readline()
       

    cont = 0
    try:
        files.remove("Amostra")
    except:
        print("An exception occurred: files.remove(\"Amostra\")")
    for nome in files:
        local = path +"/"+nome
        inst = Instancia(local)
        
        solver = Solver(path, inst.nome+".txt")

        print(inst.nome)
        print(inst.n_tarefas)
        print(inst.n_maquinas)
        print(inst.n_tarefas)
        print(inst.tp_medio)
        print(inst.setup_medio)
        print(inst.distancia_media)
        print(inst.demanda_media)
        print(inst.capacidade_media) 

        input_1 = float(inst.n_tarefas)#Tarfas
        input_2 = float(inst.n_maquinas)#Máquinas
        input_3 = float(inst.tp_medio) #tp medio                
        input_4 = float(inst.setup_medio) #setup
        input_5 = float(inst.distancia_media) # Distancia media 
        input_6 = float(inst.demanda_media)#demanda média
        input_7 = float(inst.capacidade_media)#capacidade média

        print(input_1,input_2,input_3,input_4,input_5,input_6,input_7)
       
        DataN =[np.array([input_1,input_2,input_3,input_4,input_5,input_6,input_7]).tolist()]
       
        print(DataN)
       
        D_in = np.genfromtxt(arquivoML, delimiter=',',usecols=range(1,2)).astype(float)
       
        D_in = (int)(D_in[0])
       
        print(D_in)
        #TENHO QUE MUDAR ISSO ?
        a =3
        b= 3+D_in 
       
        Base =  np.genfromtxt(arquivoML, delimiter=',',usecols=range(a,b)).astype(float).tolist() 
          
        print(Base)
       
        TestStat = stats.ttest_ind(DataN,Base,1)[1]
          
        print(TestStat)

        print(np.max(TestStat))


         #gravar (np.max(TestStat) e a instancia em um arquivo 
        arq_tolerane = open("tolerance.txt","a+")
        arq_tolerane.write(str(inst.nome))
        arq_tolerane.write(",%s"%str(np.max(TestStat)))
        arq_tolerane.write(",%s\n"%str(np.max(TestStat) < tolerance))
        arq_tolerane.close()

        if np.max(TestStat) < tolerance:
               
               Best = 1000000000000
               Rest = open(arquivoML,"a+")
               for i in range(0,len(Lista)):
                    solucao, instancia = solver.exec(0,temp_exec,Lista[i][0])
                    print("Resultado:",solucao.FO,"Estrategia:",Lista[i][0]," - ",Lista[i][1])
               
                    if solucao.FO < Best:
                        print("Best:",solucao.FO,"St:",i)
                        Best = solucao.FO
                

                        input_1 = float(instancia.n_tarefas)#Tarfas
                        input_2 = float(instancia.n_maquinas)#Máquinas
                        input_3 = float(instancia.tp_medio) #tp medio                
                        input_4 = float(instancia.setup_medio) #setup
                        input_5 = float(instancia.distancia_media) # Distancia media 
                        input_6 = float(instancia.demanda_media)#demanda média
                        input_7 = float(instancia.capacidade_media)#capacidade média
                
                        input_8 = Lista[i][0]
                    print("\n")     
        
               # Write data results
        
               print("Gravando...\n")
               #print(str(arquivo))
     
               Rest.write(str(instancia.nome))
               Rest.write(",%s"%str(7))#quant Caracteristica estatística
               Rest.write(",%s"%str(1))#quant Saidas
       
               #Caracteristica estatística
               Rest.write(",%s"%str(round(input_1,2)))
               Rest.write(",%s"%str(round(input_2,2)))
               Rest.write(",%s"%str(round(input_3,2)))
               Rest.write(",%s"%str(round(input_4,2)))
               Rest.write(",%s"%str(round(input_5,2)))
               Rest.write(",%s"%str(round(input_6,2)))
               Rest.write(",%s"%str(round(input_7,2)))

               #Saidas
               Rest.write(",%s\n"%str(input_8))       
               # Rest.write(",%s\n"%str(round(Resultado,0)))  
               Rest.close()
               
               ML(arquivoML)
               

        x = np.array([[input_1,input_2,input_3,input_4,input_5,input_6,input_7]])
    
        x_out = globals.model.predict(x)            
       
          
        input_1 = round(float(x_out[0][0]))
        #input_2 = round((x_out[0][1]))
       
         
        print("Estratégias:", input_1)
       
       
        solucao, instancia = solver.exec(0,temp_exec,input_1)
       
        # Write data results
        Rest = open(arquivoSaida,"a+")
    
        Rest.write(str(instancia.nome))
        #Rest.write(",CDC_ML")
        #Rest.write(",Str")
        Rest.write(",%s"%str(input_1))
        #Rest.write(",%s"%str(input_2))
        Rest.write(",%s"%str(solucao.FO))
        Rest.write("\n")
        Rest.close()
                             
    
      
      
