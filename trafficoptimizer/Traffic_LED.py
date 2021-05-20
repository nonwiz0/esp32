import machine, time , hcsr04
from time import sleep
from machine import Pin, PWM
from hcsr04 import HCSR04
import random

PIN_R = 25
PIN_G = 26
PIN_B = 27

PIN_R2 = 18
PIN_G2 = 19
PIN_B2 = 21
s= HCSR04(trigger_pin=13, echo_pin=12)
s2= HCSR04(trigger_pin=2, echo_pin=4)
class RGBLed:
    def __init__(self, pin_r, pin_g, pin_b):
        self.pin_r = machine.PWM(machine.Pin(pin_r))
        self.pin_g = machine.PWM(machine.Pin(pin_g))
        self.pin_b = machine.PWM(machine.Pin(pin_b))
        self.set(0, 0, 0)

    def set(self, r, g, b):
        self.r = int(r)
        self.g = int(g)
        self.b = int(b)
        self.duty()

    def duty(self):
        self.pin_r.duty(self.duty_translate(self.r))
        self.pin_g.duty(self.duty_translate(self.g))
        self.pin_b.duty(self.duty_translate(self.b))

    def duty_translate(self, n):
        """translate values from 0-255 to 0-1023"""
        return int((float(n) / 255) * 1023)

led = RGBLed(PIN_R, PIN_G, PIN_B)
led2 = RGBLed(PIN_R2, PIN_G2, PIN_B2)
#        R    G   B


    
while True:
#     led.set(255, 0, 0)
#     sleep(5)
#     led.set(0, 0, 255)
#     sleep(0.5)
#     led.set(0, 255, 0)
#     sleep(5)
#     led.set(0, 0, 255)
#     sleep(0.5)
    distance= s.distance_cm()
    distance2= s2.distance_cm()
    print('Distance:', distance,'cm')
    print('Distance2:', distance2,'cm') 
    led.set(255, 0, 0)
    led2.set(255, 0, 0)
    if distance < 10:
        sleep(0.5)
    else:
        sleep(10)    
        led.set(255, 255, 0)
        sleep(0.5)
        led.set(0, 255, 0)
        sleep(10)
        led.set(255, 255, 0)
        sleep(0.5)
