from importlib.metadata import files
from os import listdir
from os.path import *
import numpy as np
import os 
from Heuristicas.instancia import Instancia
from datetime import datetime





def read_data (path, arquivo_saida):
    
    print("criando Arquivo ... ")
    files = listar_arquivos(path)
    files.sort()
    arquivo = open(arquivo_saida, "a")
    cont = 0
    try:
        files.remove("Amostra")
    except:
        print("An exception occurred: files.remove(\"Amostra\")")

    for nome in files:
        cont += 1
        #print(nome)
        local = path +"/"+nome
        inst = Instancia(local)
        
        arquivo.write("{},{},{},{},{},{},{},{}\n".format(inst.nome,inst.n_tarefas, inst.n_maquinas,round(inst.tp_medio,2),round(inst.setup_medio,2), round(inst.distancia_media,2),round(inst.demanda_media,2),round(inst.capacidade_media,2)))

    arquivo.close()
    print("Arquivo Criado: ",arquivo_saida ," com : ",cont, " instancias" )


def listar_arquivos(caminho=None):
    lista_arqs = [arq for arq in listdir(caminho)]
    return lista_arqs


def criar_arquivo(path, arquivo):
    print("deseja excluir o arquivo? sim ou n \n", arquivo)
    resp = input()
    if resp == 'sim' or resp == 'SIM':
        lista_arqs = [arq for arq in listdir(dirname(realpath(__file__)))]
        for file in lista_arqs:
            if file == arquivo:
               os.remove(file)
        print("Arquivo Excluido: ", arquivo)
        read_data(path, arquivo) 

def recriar_arquivo(arquivo):
    print("deseja excluir o arquivo: ", arquivo, "?? sim ou n \n", arquivo)
    resp = input()
    if resp == 'sim' or resp == 'SIM':
        lista_arqs = [arq for arq in listdir(dirname(realpath(__file__)))]
        for file in lista_arqs:
            if file == arquivo:
               os.remove(file)
        print("Arquivo Excluido: ", arquivo)
    Rest = open(arquivo,"w+")
    Rest.close()

def gravar_log(exec):
    arquivoLog = "LOG_EXEC.txt"
    Rest = open(arquivoLog,"a+")
    data_e_hora_atuais = datetime.now()
    data_e_hora_em_texto = data_e_hora_atuais.strftime("%d/%m/%Y %H:%M")
    Rest.write("DATA;%s"%str(data_e_hora_em_texto))
    Rest.write(";ACAO;%s\n"%str(exec))
    Rest.close()