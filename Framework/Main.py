from Kluster import *
from Otimizacao import *
from MLS import *
from Alg import *
import globals 
import sys

from Heuristicas.solver import *
from Heuristicas.Executa_estrategias import *
from read import *

#Caminho da instancia.
path = "C:/Users/Instancias"



globals.random_state_seed = 20
random.seed(globals.random_state_seed)
#globals.initialize() 
tolerance = 0.50
globals.TolQuebra = 0.6

#O Arquivo Dados.csv contem as caracteristicas de todas as instancias.
arquivoK = "Dados.csv"
arquivoOt = "Instances.txt"
arquivoML = "Calibracao.txt"
arquivo1 = "InstanciaFolder.txt"
arquivo2 = "Instancia.txt"
arquivoSaida = "Resultados.txt"
temp_exec = 600 #em segundos




#recriar_arquivo("LOG_EXEC.txt")
#criar_arquivo(path, arquivoK)#cria o arquvo dados.csv
#recriar_arquivo(arquivoSaida)#cria o arquvo Resultados



#executar apenas as estrategias 
#recriar_arquivo("Resultados_estategias.txt")#cria o arquvo dados_matheus.csv
#executa_estrategias(path, "Resultados_estategias.txt", temp_exec)


#executar o Fremework
#ler o aquivo de log
myfile = open("LOG_EXEC.txt", "r")
next_line = myfile.readline()
ultima_exe = ""
while next_line != "" and next_line != "\n":
    next_line = next_line.rstrip('\n')
    split_line = next_line.split(';')
    ultima_exe = split_line[3]
    next_line = myfile.readline()
myfile.close()

if ultima_exe == "":
    print("Clusterizacao")	
    Clusterizacao(arquivoK) # -> gera o arquivo instances
    gravar_log("Clusterizacao")
    ultima_exe = "Clusterizacao"
    #exit()

if ultima_exe == "Clusterizacao":
    print("Otimizacao")
    Otimizacao(arquivoOt, temp_exec, path) # -> gera o arquivo Calibracão
    gravar_log("Otimizacao")
    ultima_exe = "Otimizacao"


if ultima_exe == "Otimizacao":
    print("ML")
    ML(arquivoML)
    print("ML_Solver")
    ML_Solver(path, arquivoML, arquivoSaida,tolerance, temp_exec) 
    
    gravar_log("ML_Solver")


