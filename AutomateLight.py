# Chanbroset Prach and Andreas Christian 
from rgb import RGBLed
from machine import Pin, ADC
from time import sleep

# Photoresistor sensors
p = ADC(Pin(35))
p.atten(ADC.ATTN_11DB)

Pin_R = 27
Pin_G = 25
Pin_B = 26

led = RGBLed(Pin_R, Pin_G, Pin_B)
while True:
    p_brightness = p.read()
    led_brightness = float(p_brightness * 0.0622)
    led.set(0, int(led_brightness), 0)
    
    print("LED's brightness: {} %".format((led_brightness * 100)/255 ))
    sleep(0.5)
    


