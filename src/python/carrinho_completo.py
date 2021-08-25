
"""
Created on Thu Jul 29 14:24:20 2021

@author: mathe
"""
import numpy as np
import RPi.GPIO as GPIO
import time

# Peso para PUWU e PUWD
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
pwm_1.start(0)
pwm_2.start(0)

# Pino do encoders  
encoder_1 = 11
encoder_2 = 12

GPIO.setup(encoder_1,GPIO.IN)
GPIO.setup(encoder_2,GPIO.IN)

# -- Fim da declaração dos GPIOs

# -- contadores de pulsos
pulsos_1 = 0
pulsos_2 = 0

# QTde de Pulsos de acordo com o disco
pulsos_por_volta = 20

# Intervalo para medição de dpm
intervalo = 0.5

# Variável para acionar a interrupção em ControleVelocidade
first_time = True

# Funções de callback para contagem dos pulsos
def contador_1(encoder_1):
    global pulsos_1
    pulsos_1+=1
    return

def contador_2(encoder_2):
    global pulsos_2
    pulsos_2+=1
    return

# Função de controle de velocidade
def ControleVelocidade():

    global pulsos_1
    global pulsos_2

    global first_time

    # Para diferença de tempo
    timeold = time.time()

    lista_rpm=list()

    if (first_time):
        # habilita as interrupções para contagem dos pulsos
        GPIO.add_event_detect(encoder_1, GPIO.RISING, 
            callback=contador_1, bouncetime=300)
    
        GPIO.add_event_detect(encoder_2, GPIO.RISING,
            callback=contador_2,bouncetime=300)

        first_time= False
    
    while(True):
        milliseconds = time.time()
        delta_time = milliseconds-timeold
            
        if (delta_time >=intervalo):  
            
            # pulsos/pulsos_por_volta : porçao da rotação total do motor
            rpm_1 = int((60/pulsos_por_volta)/(delta_time)*pulsos_1)
        
            rpm_2 = int((60/pulsos_por_volta)/(delta_time)*pulsos_2)
        
            timeold = time.time()
            lista_rpm.append((rpm_1,rpm_2))

            # Diferença de rpm para alteração do Dutycycle(DC)
            delta_dc = abs((rpm_1-rpm_2))*1.8

            # Se as velocidades forem diferentes, reduz a velocidade do motor com maior rpm
            if(rpm_1 not in range(rpm_2-4,rpm_2+4)):
                
                duty_cicle = 70

                if (rpm_1>rpm_2):
                    pwm_1.ChangeDutyCycle(duty_cicle-delta_dc)
                    pwm_2.ChangeDutyCycle(duty_cicle)

                else:
                    pwm_1.ChangeDutyCycle(duty_cicle+delta_dc)
                    pwm_2.ChangeDutyCycle(duty_cicle)
            
            # Se as velocidade forem iguais ou próximas    
            else:
                break

            pulsos_1=0
            pulsos_2=0
    
    try:
        rpm_final_medio = ((lista_rpm[-1][0]+lista_rpm[-1][1])/2)
    except:
        rpm_final_medio=1
    
    return rpm_final_medio

# -- Final funções de controle de velocidade

# -- Funções para A-Star Search

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
            print(ConverteParaSimbolo(num), end="")
        
        print("\n")
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

# -- FInal das funções para A-Star Search


# Função para movimentos do carrinho
def ListaMovimentos(caminho,destino):
    no = caminho[-1]
    caminho_carrinho = list()
    move_carrinho = list()

    # tempo de cada movimento
    tempo = 0
    
    while( no.anterior != None):
        caminho_carrinho.append((no.anterior.i,no.anterior.j))
        no=no.anterior
        
    caminho_carrinho=caminho_carrinho[::-1]
    caminho_carrinho.append((destino.i,destino.j))
    
    # lista de movimentos do carrinho
    for x in range(len(caminho_carrinho)-1):
        atual = caminho_carrinho[x]
        prox = caminho_carrinho[x+1]
        
        direcao = (prox[0]-atual[0], prox[1]-atual[1])
        #  Norte = 1, leste = 2, sul = 3, oeste = 4
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
    
    # Estipulando que o carrinho começa em P, virado para o sul(FRENTE POWERBANK)
    for move in move_carrinho:
        
        # 1->2: norte->leste(direita), 2->3: leste->sul(direita)
        if  (move == 2 and anterior == 1)or (move == 3 and anterior == 2):
            print("vira a direita")
            GPIO.output(Motor1A,GPIO.LOW)
            GPIO.output(Motor1B,GPIO.LOW)
            GPIO.output(Motor2A,GPIO.LOW)
            GPIO.output(Motor2B,GPIO.HIGH)

            
        # 3->2: sul->leste(esquerda), 2->1: leste->norte(esquerda)
        elif (move == 2 and anterior == 3) or (move == 1 and anterior == 2):
            print("vira a esquerda")
            
            GPIO.output(Motor1A,GPIO.LOW)
            GPIO.output(Motor1B,GPIO.HIGH)
            GPIO.output(Motor2A,GPIO.LOW)
            GPIO.output(Motor2B,GPIO.LOW)
            
            
        print("em frente")
        GPIO.output(Motor1A,GPIO.LOW)
        GPIO.output(Motor1B,GPIO.HIGH)
        GPIO.output(Motor2A,GPIO.LOW)
        GPIO.output(Motor2B,GPIO.HIGH)
        rpm = ControleVelocidade()
        
        print(rpm)
        # tempo = s/v
        # v(m/s) = 2*pi*r*rpm/60
        # s = 20cm
        # tempo = 0,2/2*3.14*raio*rpm/60

        tempo = 0.2/2*3.14*0.015*rpm/60

        time.sleep(tempo)
        anterior = move      
            
    GPIO.cleanup()
    return
# -- Final das funções de movimento do carrinho   

 
def main():
    file = '/home/pi/Documents/tcc_matheus/A_Star_Search-main/src/python/mapa_1.csv'
    
    inicio = No(0,0)
        
       
    # Carrega o arquivo
    my_data = np.genfromtxt(str(file), delimiter=';', dtype=int) 
    mapa=np.array(my_data)
   
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
