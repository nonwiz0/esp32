from machine import Pin
from machine import ADC
from time import sleep

p = ADC(Pin(35))
p.atten(ADC.ATTN_11DB)

while True:
    print(p.read())
    sleep(0.5)