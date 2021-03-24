from machine import Pin, PWM
from utime import sleep
import random

while True:
    passive_buzzer = PWM(Pin(25, Pin.OUT), freq=random.randrange(200, 400), duty=512)
    sleep(0.15)
    passive_buzzer.deinit()
    sleep(0.02)
