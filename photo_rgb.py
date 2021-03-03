# Photoresister + RGB
from rgb import RGBLed
from machine import Pin, ADC
from time import sleep
PR = 25
PG = 26
PB = 22

led = RGBLed(PR, PG, PB)
#        R    G   B
led.set(0, 0, 0)
p = ADC(Pin(35))
p.atten(ADC.ATTN_11DB)

while True:
    pr_s = p.read()
    if pr_s <= 2400:
        led.set(0, 255, 0)
    elif pr_s > 2400:
        led.set(255, 0, 0)
    print(pr_s)
    sleep(0.5)