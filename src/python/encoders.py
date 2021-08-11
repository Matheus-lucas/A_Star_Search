# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 19:00:35 2021

@author: mathe
"""

#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time 

pulsos_1 = 0
pulsos_2 = 0

pulsos_por_volta = 20

encoder_1 = 11
encoder_2 = 12

timeold = int(round(time.time() * 1000))

def contador_1(encoder_1):
    pulsos_1+=1
    return

def contador_2(encoder_2):
    pulsos_2+=1
    return

if __name__ == '__main__':
    
    GPIO.setmode(GPIO.BOARD)
    Motor1A = 16 #motor 1 frente
    Motor1B = 18 #motor 1 ré
    Motor2A = 13 #motor 2 frente
    Motor2B = 15 #motor 2 ré
 
    GPIO.setup(Motor1A,GPIO.OUT)
    GPIO.setup(Motor1B,GPIO.OUT)
    GPIO.setup(Motor2A,GPIO.OUT)
    GPIO.setup(Motor2B,GPIO.OUT)
    
    GPIO.setup(encoder_1,GPIO.IN)
    GPIO.setup(encoder_2,GPIO.IN)


    GPIO.output(Motor1A,GPIO.HIGH)
    GPIO.output(Motor1B,GPIO.LOW)
    GPIO.output(Motor2A,GPIO.HIGH)
    GPIO.output(Motor2B,GPIO.LOW)
    
    # habilita as interrpções para contar os pulsos
    GPIO.add_event_detect(encoder_1, GPIO.RISING, 
            callback=contador_1)
    
    GPIO.add_event_detect(encoder_2, GPIO.RISING,
            callback=contador_2)
    
    count=0
   
    while(count<5):
        milliseconds = int(round(time.time() * 1000))
        delta_time = milliseconds-timeold
   
    
        if (delta_time >=1000):  
          
            GPIO.remove_event_detect(encoder_1)
            GPIO.remove_event_detect(encoder_2)
            
            # 60: segundos-> minutos
            # pulsos/pulsos_por_volta : porçao da rotação total do motor
            # 1000: função millis retorna em millisegundos
            print("Pulsos 1",pulsos_1)
            rpm_1 = (60*1000/pulsos_por_volta)/(delta_time)*pulsos_1
        
            print("pULSOS 2:",pulsos_2)
            rpm_2 = (60*1000/pulsos_por_volta)/(delta_time)*pulsos_2
        
            timeold = int(round(time.time() * 1000))
            
            print("Contagem: ",count+1)
            print("RPM 1: ", rpm_1)
            print("RPM 2: ",rpm_2)
            pulsos_1=0
            pulsos_2=0
        
            # habilita as interrpções para contar os pulsos
            GPIO.add_event_detect(encoder_1, GPIO.RISING, 
                callback=contador_1)
        
            GPIO.add_event_detect(encoder_2, GPIO.RISING, 
                callback=contador_2)
            count+=1
            
    GPIO.cleanup()
    
    
    

