# -*- coding: utf-8 -*-

"""
Created on Thu Jul 29 14:24:20 2021

@author: mathe
"""
import numpy as np
import time
# Peso para PUWU e PUWD

w=10
# vetor de posições para vizinhos (norte, leste, sul, oeste)
delta = [(-1,0),(0,-1),(1,0),(0,1)]

# cria objeto nó
class No(object):
    
    def __init__(self, i=None, j=None, anterior=None, g=None, f=None):
        
        # indíces do nó
        self.i = i
        self.j = j
        
        # nó anterior
        self.anterior = anterior
        
        #custo g
        self.g = g
        
        # custo
        self.f = f

# -- Funções para A-Star Search

# Função heurística    
def Heuristica(atual, destino):
    h = 0.0
    h = abs(atual.i-destino.i)+abs(destino.j-atual.j)
    return h

# Verifica se as coordenadas estão dentro do mapa
def VerificaLimites(mapa,row, col,):
    
    return row>=0 and row<len(mapa) and col>=0 and col<len(mapa[0])


# Verifica se a célula está vazia(==0)
def CelulaVazia(mapa, row, col):

    # blocked == 1
    # Unblocked == 0
    return mapa[row][col] == 0

# Busca Vizinhos
def BuscarVizinhos(no, mapa):
    vizinhos = list()
    for posicao in delta:
        novo_i= no.i+posicao[0]
        novo_j=no.j+posicao[1]
        if(VerificaLimites(mapa, novo_i, novo_j) and CelulaVazia(mapa, novo_i, novo_j)):
            vizinhos.append(No(novo_i,novo_j))

    if vizinhos: return vizinhos
    else: 
        print("Não há vizinhos")
        return



# Verifica se o proximo vizinho é o destino
def EncontraDestino(dest, row, col):

    return row == dest.i and col == dest.j
        
# Marca o caminho(Caminho: 4, Partida: 2, Destino: 3)
def MarcarCaminho( mapa, caminho, inicio, dest, listafechada):

    for no_exp in listafechada:
        mapa[no_exp[0]][no_exp[1]]='5'

    no = caminho[-1]
    while( no.anterior != None):
        mapa[no.anterior.i][no.anterior.j]=4
        no=no.anterior
    
    mapa[inicio.i][inicio.j]= 2
    mapa[dest.i][dest.j] = 3
    
    return


# Para ordenar o vetor de fronteira
def ComparaCusto(no):
    return no.f



# Converte os valores para marcar o caminho
def ConverteParaSimbolo(e):
    if e==1: return '1'
    elif e==2: return "P"
    elif e==3: return "D"
    elif e==4: return "-"
    elif e==5: return "*"
    else: return "0"


# Colocar as marcações no mapa
def ImprimirMapa(mapa):
    for line in mapa:
        for num in line:
            print(ConverteParaSimbolo(num), end="")
        
        print("\n")
    return

# COntar o número de passos do trajeto
def ContarPassos(caminho):
    no = caminho[-1]
    contador = 1
    while( no.anterior != None):
        contador += 1
        no=no.anterior
        
    return contador

# Função de busca A* search
def a_star(inicio=None,destino=None, mapa=None, lista_custo = None, file=None  ):
   
    lista_aberta = list()
    caminho = list()
    listafechada=list()
    lista_tempo=list()
        
    trajeto_final = list()
    
    
    for func_custo in lista_custo:
        
        lista_aberta.clear()
        listafechada.clear()
        caminho.clear()
       
        atual = No()
        
        custo_g=0
        
        inicio.g = custo_g
        
        mapa_2=np.copy(mapa)
    
      
        # Define o custo da partida
        start = time.time()
        inicio.f=Heuristica(inicio, destino)
        
        lista_aberta.append(inicio)
        
        
        count=0
        
        while(not len(lista_aberta)==0):
            
            
            atual = lista_aberta[-1]
            del lista_aberta[-1]
            caminho.append(atual)
            
            # Atualiza a lista fechada
            listafechada.append((atual.i,atual.j))
            
            if((atual.i==destino.i and atual.j==destino.j) or count==100000): 
                break
        
            # Realiza a busca de vizinhos
            vizinhos = BuscarVizinhos(atual, mapa_2)
        
            # Atualização do custo g
            custo_g += 1
            
            # Se Houverem vizinhos
            if(vizinhos):
            
                for vizinho in vizinhos:
                  
                    custo_g=+1
                    
                    h = Heuristica(vizinho, destino)
                    
                    #Ponderado
                    if func_custo == 1:
                    
                        custo =    custo_g+w*h
                        
                    #pxWU
                    elif func_custo == 2:
                    
                        custo = custo_g / (2*w - 1) +h if  custo_g < (2*w - 1) *h else custo_g + h / w
                    
                    #pxWD
                    elif func_custo == 3:
                        
                        custo =  custo_g +h if  custo_g < h else (custo_g + h*(2*w-1)) / w
                    
                    #clássico
                    else:
                        custo = custo_g+h
                    
                    
                    # Verifica se aquele nó está na lista fechada   
                    try:
                        it = listafechada.index((vizinho.i,vizinho.j))
    
                    except:
                        it = -1
                    
                    if  (it ==  -1 or custo < caminho[it].f):
                        vizinho.f = custo
                        vizinho.anterior = No(i=atual.i,j=atual.j, anterior=atual.anterior, f=atual.f)
                        if (it!= -1): del caminho[it]
                        
                        lista_aberta.append(vizinho)
                        
            
            lista_aberta.sort(key=ComparaCusto, reverse=True)
            count+=1
            
        end = time.time()
        tempo = end-start
        
        passos=ContarPassos(caminho)
        
        
        trajeto_final = np.copy(caminho)
            
        lista_tempo.append([tempo,w, count, passos])
            
    
        # Marca o caminho no mapa
        MarcarCaminho(mapa_2,trajeto_final,inicio,destino, listafechada)
        ImprimirMapa(mapa_2)
        
        print("")
        
    nome = ["ponderado","pxwu","pxwd", "básico"]
    marca = 0
    
    print(lista_tempo)
    
    for elem in lista_tempo:
            
   
          print("Funcão: {}, Time: {:.5f}, w:{}, count: {}, Passos: {}".format(nome[marca],elem[0],elem[1],elem[2],elem[3]))
          marca+=1
          
# -- FInal das funções para A-Star Search
    return mapa_2, trajeto_final



def main():
    file = 'D:\TCC\src\mapas\mapas_testes\mapa_11x18.csv'
    
    inicio = No(0,0)
        
    # Carrega o arquivo
    my_data = np.genfromtxt(str(file), delimiter=';', dtype=int) 
    mapa=np.array(my_data)
   
    destino = No(len(mapa)-1,len(mapa[0])-1,f=0.0)
    
    # Validação da Partida
    if(not CelulaVazia(mapa,inicio.i,inicio.j) and VerificaLimites(mapa, inicio.i, inicio.j)): 
        print("Partida não é válida!")
        return
    
    # Validação do destino
    if(not CelulaVazia(mapa,destino.i,destino.j) and VerificaLimites(mapa, destino.i, destino.j)): 
        print("Destino não é válido!")
        return
  
    lista_custo = list()
    lista_custo =  [3,2,1,0]
    
    mapa,caminho=a_star(inicio,destino, mapa, lista_custo, file=file )    
    return
        
if __name__ == "__main__":
    main()
