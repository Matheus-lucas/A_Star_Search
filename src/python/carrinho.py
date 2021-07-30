# -*- coding: utf-8 -*-
"""
Created on Thu Jul 29 15:48:42 2021

@author: mathe
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Jul 29 14:24:20 2021

@author: mathe
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import numpy as np
from os.path import isfile, join
import os

# Peso
w=0.9

# vetor de posições para vizinhos (norte, leste, sul, oeste)
delta = [(-1,0),(0,-1),(1,0),(0,1)]

# cria objeto nó
class No(object):
    
    def __init__(self, i=None, j=None, anterior=None, f=None):
        
        # indíces do nó
        self.i = i
        self.j = j
        
        # nó anterior
        self.anterior = anterior
        
        # custo
        self.f = f

# funçaõ heurística    
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



# Verifica se o proximo vizinho é válido
def EncontraDestino(dest, row, col):

    return row == dest.i and col == dest.j
        
# marca o caminho
def MarcarCaminho( mapa, caminho, inicio, dest):
    
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
    else: return "0"
    
# Colocar as marcações no mapa
def ImprimirMapa(mapa):
    for line in mapa:
        for num in line:
            print(ConverteParaSimbolo(num),end="")
        
        print("\n")
    return

# Salvar o mapa como arquivo csv
def salvar_mapa(mapa,file):
    mapa_2=np.copy(mapa)
    newpath = 'D:/TCC/src/mapas/mapas_filtrados_2'
    new_file = join(newpath,file)
    pd.DataFrame(mapa_2).to_csv(new_file, header=None, index=None,sep=";")
    return

# funçaõ de busca A* search
def a_star(inicio=None,destino=None, mapa=None, file=None):
    fronteira = list()
    atual = No()
    caminho = list()
    custo_g=0
    mapa_2=np.copy(mapa)
      
    inicio.f=Heuristica(inicio, destino)
    
    fronteira.append(inicio)
    listafechada=list()
    
    count=1
    while(not len(fronteira)==0):
      
        #print("{:.1f} %".format(count/100000), end="\r")
        
        atual = fronteira[-1]
        del fronteira[-1]
        caminho.append(atual)
        
        if((atual.i==destino.i and atual.j==destino.j) or count==50000): 
            break
    
        
        vizinhos = BuscarVizinhos(atual, mapa_2)
        custo_g+=1
        
        # Atualiza a lista fechada
        listafechada.append((atual.i,atual.j))
        
        if(vizinhos):
        
            for vizinho in vizinhos:
                custo_g+=1
                h = Heuristica(vizinho, destino)
                
                #puWU
                #custo = custo_g / (2*w - 1) +h if  custo_g < (2*w - 1) *h else custo_g + h / w
                    
                
                #puWD
                custo =  custo_g +h if  custo_g < h else (custo_g + h*(2*w-1)) / w
                    
                # Verifica se aquele nó está na lista fechada   
                try:
                    it = listafechada.index((vizinho.i,vizinho.j))

                except:
                    it = -1
                
                if  (it ==  -1 or custo < caminho[it].f):
                    vizinho.f = custo
                    vizinho.anterior = No(i=atual.i,j=atual.j, anterior=atual.anterior,f=atual.f)
                    if (it!= -1): del caminho[it]
                    
                    fronteira.append(vizinho)
        
        fronteira.sort(key=ComparaCusto, reverse=True)
        count+=1
    
    MarcarCaminho(mapa_2,caminho,inicio,destino)
    ImprimirMapa(mapa_2)
    print(count)
    return mapa_2,caminho

def MoveCarrinho(tipo):
    if tipo==1:
        print("frente")
        
    elif tipo==2:
        print("tras")
        
    elif tipo==3:
        print("desce")
        
    else:
        print("sobe")
        

def ListaMovimentos(caminho,destino):
    no = caminho[-1]
    caminho_carrinho = list()
    move_carrinho = list()
    while( no.anterior != None):
        caminho_carrinho.append((no.anterior.i,no.anterior.j))
        no=no.anterior
        
    caminho_carrinho=caminho_carrinho[::-1]
    caminho_carrinho.append((destino.i,destino.j))
    
    # lista de movimentos do carrinho
    for x in range(len(caminho_carrinho)-1):
        atual = caminho_carrinho[x]
        prox = caminho_carrinho[x+1]
        move_carrinho.append((prox[0]-atual[0], prox[1]-atual[1]))
    
    
    print("Carrinho")
    print(move_carrinho)
    for move in move_carrinho:
        if move == (0,1):
            MoveCarrinho(1)
            
        elif move == (0,-1):
            MoveCarrinho(2)
            
        elif move == (1,0):
            MoveCarrinho(3)
    
        else: MoveCarrinho(4)
    return
    
  
    
    
    
    
def main():
    file = 'D:/TCC/src/mapas/mapas_filtrados/mapa_11x18.csv'  
    
    inicio = No(0,0)
        
       
    # Carrega o arquivo
    mapa=pd.read_csv(str(file), header=None, delimiter=";") 
    mapa=np.array(mapa)
    #mapa=mapa[:,:-1]
   
    print(mapa)
    destino = No(len(mapa)-1,len(mapa[0])-1,f=0.0)
    
    # Validação do inicio e Partida
    if(not CelulaVazia(mapa,inicio.i,inicio.j) and VerificaLimites(mapa, inicio.i, inicio.j)): 
        print("Partida não é válida!")
        return
    
    if(not CelulaVazia(mapa,destino.i,destino.j) and VerificaLimites(mapa, destino.i, destino.j)): 
        print("Destino não é válido!")
        return
  
    mapa,caminho= a_star(inicio,destino, mapa,file=file)    
    ListaMovimentos(caminho, destino)
    return
        

if __name__ == "__main__":
    main()











