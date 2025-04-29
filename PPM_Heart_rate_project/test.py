from led     import Led
from time    import sleep
from machine import Pin, ADC, I2C
from fifo    import Fifo

adc = ADC(26)
while True:    
    print(adc.read_u16())
    sleep(0.05)