
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
    
    def __init__(self, i=None, j=None, anterior=None, f=None):
        
        # indíces do nó
        self.i = i
        self.j = j
        
        # nó anterior
        self.anterior = anterior
        
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
            print(ConverteParaSimbolo(num), end="")
        
        print("\n")
    return

# Função de busca A* search
def a_star(inicio=None,destino=None, mapa=None, file=None):
    fronteira = list()
    atual = No()
    caminho = list()
    custo_g=0
    mapa_2=np.copy(mapa)
      
    # Define o custo da partida
    start = time.time()
    inicio.f=Heuristica(inicio, destino)
    
    fronteira.append(inicio)
    listafechada=list()
    
    count=0
    while(not len(fronteira)==0):
        
        atual = fronteira[-1]
        del fronteira[-1]
        caminho.append(atual)
        
        if((atual.i==destino.i and atual.j==destino.j) or count==100000): 
            break
    
        # Realiza a busca de vizinhos
        vizinhos = BuscarVizinhos(atual, mapa_2)
        
        custo_g+=1
        
        # Atualiza a lista fechada
        listafechada.append((atual.i,atual.j))
        
        # Se Houverem vizinhos
        if(vizinhos):
        
            for vizinho in vizinhos:
                
                count+=1
                h = Heuristica(vizinho, destino)
                
                #clássico
                #custo = custo_g+h
                
                #Ponderado
                custo =    custo_g+w*h
                
                #puWU
                #custo = custo_g / (2*w - 1) +h if  custo_g < (2*w - 1) *h else custo_g + h / w
                
                #puWD
                #custo =  custo_g +h if  custo_g < h else (custo_g + h*(2*w-1)) / w
                
                
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
        
    end = time.time()
    
    # Marca o caminho no mapa
    MarcarCaminho(mapa_2,caminho,inicio,destino)
    ImprimirMapa(mapa_2)
    print(count)
    print("Time: {:.5f}".format(end-start))
    return mapa_2,caminho

# -- FInal das funções para A-Star Search



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
  
    
    mapa,caminho= a_star(inicio,destino, mapa,file=file)    
    return
        
if __name__ == "__main__":
    main()
