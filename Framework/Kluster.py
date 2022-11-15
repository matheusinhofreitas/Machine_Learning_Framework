import seaborn as sns  
from sklearn.cluster import KMeans
import pandas as pd
import matplotlib.pyplot as plt
import math
import csv
import random
from operator import itemgetter 
import globals 


def calculate_wcss(data,range_n_clusters):
    wcss = []
    for n in range_n_clusters:
        kmeans = KMeans(n_clusters=n, random_state = globals.random_state_seed)
        kmeans.fit(X=data)
        wcss.append(kmeans.inertia_)

    return wcss
    
    
def optimal_number_of_clusters(wcss,Dim,ClusterMax):
    x1, y1 = Dim, wcss[0]
    x2, y2 = ClusterMax-1, wcss[len(wcss)-1]

    distances = []
    for i in range(len(wcss)):
        x0 = i+2
        y0 = wcss[i]
        numerator = abs((y2-y1)*x0 - (x2-x1)*y0 + x2*y1 - y2*x1)
        denominator = math.sqrt((y2 - y1)**2 + (x2 - x1)**2)
        distances.append(numerator/denominator)
    
    return distances.index(max(distances)) + 2

def Clusterizacao (Files):

    #arquivo = "Dados.csv"
    arquivo = Files
    #open file with pd.read_csv
    df = pd.read_csv(arquivo)
    
    dfDados = df.iloc[:, 1:]
    
    print(dfDados.head())
    
    
    Dim = dfDados.shape[1] #Number of variable of the data set
    DimN = dfDados.shape[0]
    #ClusterMax = round(0.005*DimN)
    ClusterMax = round(0.1*DimN)
    
    print("ClusterMax: \n",ClusterMax)
    
    range_n_clusters = list(range(Dim,Dim+ClusterMax))   
    
    
    # calculating the within clusters sum-of-squares for 19 cluster amounts
    sum_of_squares = calculate_wcss(dfDados,range_n_clusters)
    
    # calculating the optimal number of clusters
    n = optimal_number_of_clusters(sum_of_squares,Dim,ClusterMax)
    
    print("Otimo: \n", n)
    
    plt.plot(range_n_clusters, sum_of_squares, 'bx-')
    plt.xlabel('k')
    plt.ylabel('Sum_of_squared_distances')
    plt.title('Elbow Method For Optimal k')
    #plt.show()
    
    # running kmeans to our optimal number of clusters
    kmeans = KMeans(n_clusters=n, n_init=n, random_state=globals.random_state_seed).fit(dfDados)
    
    labels = kmeans.predict(dfDados)
    
    print(labels)
    
    df.insert(Dim+1, "Kluster", labels, True)
    
    print(df.head(20))
    
    df.to_csv("DatasetK.csv")
    
    df = pd.read_csv("DatasetK.csv")
    
    grouped_df = df.groupby('Kluster').apply(lambda x :x.iloc[random.choice(range(0,len(x)))])
    
    print(grouped_df)
    
    keys, values = zip(*grouped_df.items()) # Split values
    
    Instances = values[1]
    print(Instances)
    
    Rest = open("Instances.txt","w+")
    for i in range(len(Instances)):
        Rest.write("%s"%Instances[i])
        Rest.write("\n")   
    