from utime import sleep
from machine import Pin, ADC

p = ADC(Pin(35))
p.atten(ADC.ATTN_11DB)

while True:
    print(p.read())
    sleep(1)
