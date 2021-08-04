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

w=0.9

delta = [(-1,0),(0,-1),(1,0),(0,1)]
class No(object):
    
    def __init__(self, i=None, j=None, anterior=None, f=None):
        self.i = i
        self.j = j
        
        self.anterior = anterior
        
        self.f = f

    
def Heuristica(atual, destino):
    h = 0.0
    h = abs(atual.i-destino.i)+abs(destino.j-atual.j)
    return h


def VerificaLimites(mapa,row, col,):
    
    return row>=0 and row<len(mapa) and col>=0 and col<len(mapa[0])


## Verify if the the cell is blocked
def CelulaVazia(mapa, row, col):

    # blocked == 1
    # Unblocked == 0
    return mapa[row][col] == 0

#Bsuca Vizinhos
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



# Verify if the next cell is destination
def EncontraDestino(dest, row, col):

    return row == dest.i and col == dest.j
        

def MarcarCaminho( mapa, caminho, inicio, dest):
    
    no = caminho[-1]
    while( no.anterior != None):
        mapa[no.anterior.i][no.anterior.j]=4
        no=no.anterior
    
    mapa[inicio.i][inicio.j]= 2
    mapa[dest.i][dest.j] = 3
    return


def ComparaCusto(no):
    return no.f


def ConverteParaSimbolo(e):
    if e==1: return '1'
    elif e==2: return "P"
    elif e==3: return "D"
    elif e==4: return "-"
    else: return "0"
    
def ImprimirMapa(mapa):
    for line in mapa:
        for num in line:
            print(ConverteParaSimbolo(num),end="")
        
        print("\n")
    return

def salvar_mapa(mapa,file):
    mapa_2=np.copy(mapa)
    newpath = 'D:/TCC/src/pythonmapa_1.csv'
    new_file = join(newpath,file)
    pd.DataFrame(mapa_2).to_csv(new_file, header=None, index=None,sep=";")
    return

def a_star(inicio=None,destino=None, mapa=None, file=None,tipo=None):
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
        print(count)
        #print("{:.1f} %".format(count/100000), end="\r")
        
        atual = fronteira[-1]
        del fronteira[-1]
        caminho.append(atual)
        
        if((atual.i==destino.i and atual.j==destino.j) or count==50000): 
            break
    
        
        vizinhos = BuscarVizinhos(atual, mapa_2)
        custo_g+=1
        
        listafechada.append((atual.i,atual.j))
        
        if(vizinhos):
        
            for vizinho in vizinhos:
                #custo_g+=1
                h = Heuristica(vizinho, destino)
                
                """if tipo == 1:
                    # Ponderado
                    custo = custo_g+w*h
                    
                elif tipo==2:
                    # Ponderado 2
                    custo=(1-w)*custo_g+w*h
                    
                elif tipo==3:
                    # puWU"""
                custo = custo_g / (2*w - 1) +h if  custo_g < (2*w - 1) *h else custo_g + h / w
                    
                #elif tipo==4:
                    #puWD"""
                #custo =  custo_g +h if  custo_g < h else (custo_g + h*(2*w-1)) / w
                    
                #else:
                   # custo = custo_g+h
                    
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
    return mapa_2

def main():
    file = 'D:/TCC/src/python/mapa_1.csv'  
    
    inicio = No(0,0)
        
       
    # Carrega o arquivo
    mapa=pd.read_csv(str(file), header=None, delimiter=";") 
    mapa=np.array(mapa)
    #mapa=mapa[:,:-1]
   
    print(mapa)
    dest = No(len(mapa)-1,len(mapa[0])-1,f=0.0)
    
    # Validação do inicio e Partira
    if(not CelulaVazia(mapa,inicio.i,inicio.j) and VerificaLimites(mapa, inicio.i, inicio.j)): 
        print("Partida não é válida!")
        return
    
    if(not CelulaVazia(mapa,dest.i,dest.j) and VerificaLimites(mapa, dest.i, dest.j)): 
        print("Destino não é válido!")
        return
  
    caminho=a_star(inicio,dest, mapa,file=file, tipo=4)    
    return
        

if __name__ == "__main__":
    main()











