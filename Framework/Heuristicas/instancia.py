#class A(object):
#    def __init__(self):
#        print("init")
#    def __call__(self):
#        print("call ")

#a = A() #imprime init
#a() #imprime call
import numpy as np
import statistics

class Instancia:
    local = ''
    nome = ''
    grupo = 0
    n_tarefas = 0
    n_veiculos = 0
    n_maquinas = 0


    tempo_viagem = []# tempo_viagem[local_j][local_k]. = IGUAL A DISTANCIA
    tempo_processamento= [] # tempoProcessamento[maquina][tarefa].
    tempo_setup = [] # tempo_setup[maquina][tarefa][tarefa].
    penalidade_atraso = [] # penalidade_atraso[tarefa].
    data_entrega = []# data_entrega[tarefa].
    tamanho_tarefa = []# tamanho_tarefa[tarefa].
    capacidade_veiculo = []# capacidade_veiculo[veiculo].
    velocidade_veiculos = []#Velocidade do veiculo
    #informações sobre as instancias
    capacidade_total = 0
    demanda_total = 0
    setup_min = 0
    setup_max = 0
    raio = 0
    circulos = 0
    tempo_processamento_min = 0
    tempo_processamento_max = 0
    demanda_min = 0
    demanda_max = 0
    priority_factor = 0
    range_factor_R = 0
    u_factor = 0.5
    alpha = 0.1
    replicacao = 0


    #estatisticas da Instancia
    tp_medio = 0
    setup_medio = 0
    distancia_media = 0
    demanda_media = 0
    capacidade_media = 0

    #construtor
    def __init__(self, local):
        self.local = local
        self.carregar_instancia()
        self.calcula_estatistica()
        #self.imprimir_instancia()
        #print("init")


    #def __call__(self):
    #    print("call ")

    #metodos
    def calcula_estatistica (self):
        self.tp_medio = np.average(self.tempo_processamento)
        self.setup_medio = np.average(self.tempo_setup)
        self.distancia_media = np.average(self.tempo_viagem)
        self.demanda_media = np.average(self.tamanho_tarefa)
        self.capacidade_media = np.average(self.capacidade_veiculo)

    def carregar_instancia(self):
        aux_nome = self.local.split('/')
        aux_nome = aux_nome[len(aux_nome)-1].split('.')
        self.nome = aux_nome[0]
        arquivo = open(self.local, 'r')

        #numero de maquinas
        linha = arquivo.readline()
        linha = linha.strip()
        aux = linha.split(':')
        self.n_maquinas = (int)(aux[1])


        #numero Tarefas
        linha = arquivo.readline()
        linha = linha.strip()
        aux = linha.split(':')
        self.n_tarefas = (int)(aux[1])


        #numero veiculos
        linha = arquivo.readline()
        linha = linha.strip()
        aux = linha.split(':')
        self.n_veiculos = (int)(aux[1])


        linha = arquivo.readline() #Capacidade_Total
        linha = arquivo.readline() #Demanda total
        linha = arquivo.readline() #setup min
        linha = arquivo.readline() #setup max
        linha = arquivo.readline() #Raio
        linha = arquivo.readline() #circulos
        linha = arquivo.readline() #TP min
        linha = arquivo.readline() #TP max
        linha = arquivo.readline() #Demanda_Min
        linha = arquivo.readline() #Priority_Factor
        linha = arquivo.readline() #Range_Factor_R
        linha = arquivo.readline() #U_factor
        linha = arquivo.readline() #Alpha
        linha = arquivo.readline() #Alpha



        #ENTRADA ANTIGAS
        #Tempos de processamento
        linha = arquivo.readline()
        self.tempo_processamento = np.zeros((self.n_maquinas, (self.n_tarefas + 1)))
        for j in range(0, self.n_tarefas + 1):
            linha = arquivo.readline()
            linha = linha.strip()
            linha = linha.split("\t")
            k = 1
            for i in range(0, self.n_maquinas):
                self.tempo_processamento[i][j] = int (linha[k]);
                k = k + 2
        linha = arquivo.readline()


        # Tempos de processamento
        #linha = arquivo.readline()
        #self.tempo_processamento = np.zeros((self.n_maquinas, (self.n_tarefas + 1)))
        #for i in range(0, self.n_maquinas):
        #    linha = arquivo.readline()
        #    linha = linha.strip()
        #    linha = linha.split("\t")
        #    for j in range(0, self.n_tarefas + 1):
        #        self.tempo_processamento[i][j] = linha[j];




        #Tempos de setup
        linha = arquivo.readline()
        self.tempo_setup = np.zeros((self.n_maquinas, self.n_tarefas+1, self.n_tarefas+1))
        for i in range(0, self.n_maquinas):
            linha = arquivo.readline()
            for j in range(0, self.n_tarefas + 1):
                linha = arquivo.readline()
                linha = linha.strip()
                linha = linha.split("\t")
               # print(linha)
                for k in range(0, self.n_tarefas + 1):
                    self.tempo_setup[i][j][k] = linha[k]



        # tamanho das tarefas
        linha = arquivo.readline()
        self.tamanho_tarefa = np.zeros(self.n_tarefas + 1)
        linha = arquivo.readline()
        linha = linha.strip()
        linha = linha.split("\t")
        for j in range(0, self.n_tarefas + 1):
            self.tamanho_tarefa[j] = linha[j]



        # datas de entregas
        linha = arquivo.readline()
        self.data_entrega = np.zeros(self.n_tarefas + 1)
        linha = arquivo.readline()
        linha = linha.strip()
        linha = linha.split("\t")
        for j in range(0, self.n_tarefas + 1):
            self.data_entrega[j] = linha[j]


        # penalidade de atraso
        linha = arquivo.readline()
        self.penalidade_atraso = np.zeros(self.n_tarefas + 1)
        linha = arquivo.readline()
        linha = linha.strip()
        linha = linha.split("\t")
        for j in range(0, self.n_tarefas + 1):
            self.penalidade_atraso[j] = linha[j]



        # Capacidade dos veiculos
        linha = arquivo.readline()
        self.capacidade_veiculo = np.zeros(self.n_veiculos)
        linha = arquivo.readline()
        linha = linha.strip()
        linha = linha.split("\t")
        for j in range(0, self.n_veiculos):
            self.capacidade_veiculo[j] = linha[j]

        linha = arquivo.readline()  # Custo_Fixo_Veiculo
        linha = arquivo.readline()  # Coordenadas_Clientes
        linha = arquivo.readline()  # Coordenadas_Clientes
        for j in range(0, self.n_tarefas +1 ): #coordenadas dos clientes
            linha = arquivo.readline()

        # Tempos de viagem
        linha = arquivo.readline()
        self.tempo_viagem = np.zeros((self.n_tarefas + 1, self.n_tarefas + 1))
        for j in range(0, self.n_tarefas + 1):
            linha = arquivo.readline()
            linha = linha.strip()
            linha = linha.split("\t")
            for k in range(0, self.n_tarefas + 1):
               self.tempo_viagem[j][k] = int(linha[k])

        linha = arquivo.readline()  # Custo_Viagem
        for i in range(0, self.n_veiculos):
            linha = arquivo.readline()  # Custo_Viagem
            for j in range(0, self.n_tarefas + 1):
                linha = arquivo.readline()  # Custo_Viagem

        # Velocidade dos veiculos
        linha = arquivo.readline()
        self.velocidade_veiculos = np.zeros(self.n_veiculos)
        linha = arquivo.readline()
        linha = linha.strip()
        linha = linha.split("\t")
        for j in range(0, self.n_veiculos):
            self.velocidade_veiculos[j] = int(linha[j])


    def imprimir_instancia(self):
        print("numero maquinas: {}".format(self.n_maquinas))
        print("numero tarefas: {}".format(self.n_tarefas))
        print("numero veiculo: {}".format(self.n_veiculos))
        print("tempos de processamento")
        print(self.tempo_processamento)
        print("tempos de setup")
        print(self.tempo_setup)
        print("tamanho das tarefas")
        print(self.tamanho_tarefa)
        print("Datas de entrega")
        print(self.data_entrega)
        print("penalidade de atraso")
        print(self.penalidade_atraso)
        print("capacidade dos veiculos")
        print(self.capacidade_veiculo)
        print("tempos de Viagem")
        print(self.tempo_viagem)
        print("velocidade dos veiculos")
        print(self.velocidade_veiculos)