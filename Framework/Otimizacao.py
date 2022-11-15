import statistics
#from CDC import *
import numpy as np
import globals
from Heuristicas.solver import *

def Leitura(nomeArq):

 #Leitura do arquivo
 filename = nomeArq
 dadoE=[]

 with open(filename) as f:
    content = f.read().splitlines()
    for line in content:
        contentBreak = line.split()
        for temp in contentBreak:
            dadoE.append(temp)

 n1 = int(dadoE[0])
 n2 = int(dadoE[1])
 maq1 = int(dadoE[2])
 maq2 = int(dadoE[3])
 p1=[]
 p2=[]
 Q1=[]
 Q2=[]

 ind = 0

 for item in range(4,4+n1,1):
    p1.append(int(dadoE[item]))

 for item in range(4+n1,4+n1+n2,1):
    p2.append(int(dadoE[item]))

 Prec = np.zeros(shape=(n2, n1), dtype=int)

 for i in range(0,n2):
   for j in range(4+n1*(i+1)+n2, 4+n1*(i+1)+n2+n1):
     Prec[i,j-(4+n1*(i+1)+n2)]=int(dadoE[j])
     
 for i in range(4+n1*(i+1)+n2+n1,4+n1*(i+1)+n2+n1+maq1):
     Q1.append(float(dadoE[i]))
     
 for j in range(4+n1*(i+1)+n2+n1+maq1,4+n1*(i+1)+n2+n1+maq1+maq2):
     Q2.append(float(dadoE[i]))

 return n1,n2,maq1,maq2,p1,p2,Prec,Q1,Q2



def Otimizacao(Instancias, temp_exec, path):

    
    ###################################################################################################
    # The objective function is what will be optimized.
    Rest = open("Calibracao.txt","w+")
    myfile = open(Instancias)   #open('Instances.txt')
    next_line = myfile.readline()
    
    while next_line != "" and next_line != "\n":
     
       arquivo = next_line
       arquivo = arquivo.replace("\n", "").replace(" ", "")
    
       print(arquivo)
    
     
    
       
       
       Lista = []
       Lista.append((0,"BL d_linha"))
       Lista.append((1,"BL p_linha"))
       Lista.append((2,"BL p+d"))
       Lista.append((3,"BL p+d Rest"))

      
       Best = 1000000000000
       solver = Solver(path, arquivo+".txt")
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
     
       Rest.write(str(arquivo))
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
     
       next_line = myfile.readline()






