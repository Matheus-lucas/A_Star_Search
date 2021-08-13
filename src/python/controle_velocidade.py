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

timeold = time.time()

def contador_1(encoder_1):
    global pulsos_1
    pulsos_1+=1
    return

def contador_2(encoder_2):
    global pulsos_2
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
    
    pwm_1 = GPIO.PWM(Motor1A,100)
    pwm_2 = GPIO.PWM(Motor2A,100)
    
    GPIO.setup(encoder_1,GPIO.IN)
    GPIO.setup(encoder_2,GPIO.IN)


    GPIO.output(Motor1A,GPIO.HIGH)
    GPIO.output(Motor1B,GPIO.LOW)
    GPIO.output(Motor2A,GPIO.HIGH)
    GPIO.output(Motor2B,GPIO.LOW)
    
    lista_rpm=list()
    # habilita as interrpções para contar os pulsos
    GPIO.add_event_detect(encoder_1, GPIO.RISING, 
            callback=contador_1)
    
    GPIO.add_event_detect(encoder_2, GPIO.RISING,
            callback=contador_2)
    
    count=0
    try:
        while(count<5):
            milliseconds = time.time()
            delta_time = milliseconds-timeold
            
            if(delta_time <0):
                GPIO.cleanup()
                
            if (delta_time >=2):  
              
                #GPIO.remove_event_detect(encoder_1)
                #GPIO.remove_event_detect(encoder_2)
                
                
                # pulsos/pulsos_por_volta : porçao da rotação total do motor
                rpm_1 = round((60/pulsos_por_volta)/(delta_time)*pulsos_1,3)
            
                rpm_2 = round((60/pulsos_por_volta)/(delta_time)*pulsos_2,3)
            
                timeold = time.time()
                
                if(rpm_1 != rpm_2):
                    
                    duty_cicle = int(100*min(rpm_1,rpm_2)/(max(rpm_1,rpm_2)))
                    
                    
                    
                    pwm_1.start(0)
                    pwm_2.start(0)
                    
                    pwm_1.ChangeDutyCycle(duty_cicle)
                    pwm_2.ChangeDutyCycle(duty_cicle)
                
                pulsos_1=0
                pulsos_2=0
            
                # habilita as interrpções para contar os pulsos
                '''GPIO.add_event_detect(encoder_1, GPIO.RISING, 
                    callback=contador_1)
            
                GPIO.add_event_detect(encoder_2, GPIO.RISING, 
                    callback=contador_2)'''
                count+=1
                lista_rpm.append((round(rpm_1),(rpm_2)))
                
        GPIO.cleanup()
        print(lista_rpm)
    
    except:
        print(lista_rpm)
        GPIO.cleanup()
    
