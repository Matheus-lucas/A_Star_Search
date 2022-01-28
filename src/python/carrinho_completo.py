
"""
Created on Thu Jul 29 14:24:20 2021

@author: mathe
"""
import numpy as np
import RPi.GPIO as GPIO
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



# --Declaração do GPIO
GPIO.setmode(GPIO.BOARD)

#FRENTE POWERBANK
#Motores
Motor1A = 16 #motor 1 RÉ
Motor1B = 18 #motor 1 FRENTE
Motor2A = 13 #motor 2 RÉ
Motor2B = 15 #motor 2 FRENTE
 
GPIO.setup(Motor1A,GPIO.OUT)
GPIO.setup(Motor1B,GPIO.OUT)
GPIO.setup(Motor2A,GPIO.OUT)
GPIO.setup(Motor2B,GPIO.OUT)

#PWM
pwm_1 = GPIO.PWM(Motor1A,100)
pwm_2 = GPIO.PWM(Motor2A,100)

pwm_1.ChangeDutyCycle(90)
pwm_2.ChangeDutyCycle(80)
#pw2_1.start(80)
#pwm_2.start(60)

# Pino do encoders  
encoder_1 = 11
encoder_2 = 12

GPIO.setup(encoder_1,GPIO.IN)
GPIO.setup(encoder_2,GPIO.IN)

# -- Fim da declaração dos GPIOs

# -- Variáveis para controle de velocidade

# contadores de pulsos
pulsos_1 = 0
pulsos_2 = 0

# QTde de Pulsos de acordo com o disco
pulsos_por_volta = 20

# Intervalo para medição de pm
intervalo = 0.1

# Variável para acionar a interrupção em ControleVelocidade
first_time = True
# -- Fim das variáveis

# -- Funções para controle de velocidade
# Função de controle de velocidade

#Função de parada
def stop():
    GPIO.output(Motor1A,GPIO.LOW)
    GPIO.output(Motor1B,GPIO.LOW)
    GPIO.output(Motor2A,GPIO.LOW)
    GPIO.output(Motor2B,GPIO.LOW)
    time.sleep(0.5)

    return

# -- Final funções de controle de velocidade

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
    inicio.f=Heuristica(inicio, destino)
    
    fronteira.append(inicio)
    listafechada=list()
    
    count=1
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
                custo_g+=1
                h = Heuristica(vizinho, destino)
                
                
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
    
    # Marca o caminho no mapa
    MarcarCaminho(mapa_2,caminho,inicio,destino)
    ImprimirMapa(mapa_2)
    print(count)
    return mapa_2,caminho

# -- FInal das funções para A-Star Search


# Função para movimentos do carrinho
def ListaMovimentos(caminho,destino):
    no = caminho[-1]
    caminho_carrinho = list()
    move_carrinho = list()

    # tempo de cada movimento
    
    # ir pra frente
    tempo_frente = 0.75
    
    #vira a esquerda
    tempo_esquerda = 0.65
    
    #vira a direita
    tempo_direita = 0.7
    
    #Movimento lateral
    tempo_lateral =  0.7
    
    tempo_recuo = 0.35
    
    # Desempacotando o caminho
    while( no.anterior != None):
        caminho_carrinho.append((no.anterior.i,no.anterior.j))
        no=no.anterior
        
    # Reverte o vetor caminho
    caminho_carrinho=caminho_carrinho[::-1]

    # Inclui destino no caminho
    caminho_carrinho.append((destino.i,destino.j))
    
    # Lista de movimentos do carrinho
    for x in range(len(caminho_carrinho)-1):
        atual = caminho_carrinho[x]
        prox = caminho_carrinho[x+1]
        
        # Norte -> direção = (-1,0)
        # Leste -> direção = (0,1)
        # Sul -> direção = (1,0)
        # Oeste -> direção = (-1,0)
        direcao = (prox[0]-atual[0], prox[1]-atual[1])
        
        #  Norte = 1, Leste = 2, Sul = 3, Oeste = 4
        if direcao == (-1,0):
            move_carrinho.append(1)
            
        elif direcao == (0,1):
            move_carrinho.append(2)
            
        elif direcao == (1,0):
            move_carrinho.append(3)
            
        else:
            move_carrinho.append(4)
    
    
    #print("Carrinho")
    #print(move_carrinho)
    anterior = 0
    try:
    
        # Estipulando que o carrinho começa em P, virado para o sul(FRENTE POWERBANK)
        for move in move_carrinho:
            
            # 1->2: Norte->Leste(direita), 2->3: Leste->Sul(direita);3->4: sul->oeste(direita)
            if  (move == 2 and anterior == 1)or (move == 3 and anterior == 2) or (move==4 and anterior==3):
                #Vira a direita
                
                GPIO.output(Motor1A,GPIO.HIGH)
                GPIO.output(Motor1B,GPIO.LOW)
                GPIO.output(Motor2A,GPIO.HIGH)
                GPIO.output(Motor2B,GPIO.LOW)
                time.sleep(tempo_recuo)
                stop()
                
                GPIO.output(Motor1A,GPIO.LOW)
                GPIO.output(Motor1B,GPIO.LOW)
                GPIO.output(Motor2A,GPIO.LOW)
                GPIO.output(Motor2B,GPIO.HIGH)
                time.sleep(tempo_direita)
                stop()

                
            # 3->2: Sul->leste(esquerda), 2->1: Leste->Norte(esquerda); 4->3: oeste->sul(esquerda)
            elif (move == 2 and anterior == 3) or (move == 1 and anterior == 2) or(move==3 and anterior==4):
                
                #Vira a esquerda
                GPIO.output(Motor1A,GPIO.HIGH)
                GPIO.output(Motor1B,GPIO.LOW)
                GPIO.output(Motor2A,GPIO.HIGH)
                GPIO.output(Motor2B,GPIO.LOW)
                time.sleep(tempo_recuo)
                stop()
                
                GPIO.output(Motor1A,GPIO.LOW)
                GPIO.output(Motor1B,GPIO.HIGH)
                GPIO.output(Motor2A,GPIO.LOW)
                GPIO.output(Motor2B,GPIO.LOW)
                time.sleep(tempo_esquerda)
                stop()
                
                
            #em frente
            GPIO.output(Motor1A,GPIO.LOW)
            GPIO.output(Motor1B,GPIO.HIGH)
            GPIO.output(Motor2A,GPIO.LOW)
            GPIO.output(Motor2B,GPIO.HIGH)
            
            
            if move==1 or move ==3:
                tempo=tempo_frente
                
            else:
                tempo=tempo_lateral
            time.sleep(tempo)
            
            stop()
            
            #GPIO.output(Motor1A,GPIO.HIGH)
            #GPIO.output(Motor1B,GPIO.LOW)
            #GPIO.output(Motor1A,GPIO.LOW)
            #GPIO.output(Motor1B,GPIO.HIGH)
            #time.sleep(0.1)
            anterior = move
            

        pwm_1.stop()
        pwm_2.stop()
        GPIO.cleanup()
        
    except:
        pwm_1.stop()
        pwm_2.stop()
        GPIO.cleanup()

    return
# -- Final das funções de movimento do carrinho   

 
def main():
    file = '/home/pi/Documents/tcc_matheus/A_Star_Search-main/src/python/mapa_5x5_reto.csv'
    
    # Carrega o arquivo
    my_data = np.genfromtxt(str(file), delimiter=';', dtype=int) 
    mapa=np.array(my_data)
    
    inicio = No(0,0)
   
    destino = No(4,4,f=0.0)
    # Validação da Partida
    if(not CelulaVazia(mapa,inicio.i,inicio.j) and VerificaLimites(mapa, inicio.i, inicio.j)): 
        print("Partida não é válida!")
        return
    
    # Validação do destino
    if(not CelulaVazia(mapa,destino.i,destino.j) and VerificaLimites(mapa, destino.i, destino.j)): 
        print("Destino não é válido!")
        return
  
    mapa,caminho= a_star(inicio,destino, mapa,file=file)    
    ListaMovimentos(caminho, destino)
    return
        
if __name__ == "__main__":
    main()
