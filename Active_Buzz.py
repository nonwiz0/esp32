# Andreas Christian Mambu and Chanbroset Prach
from machine import Pin
from utime import sleep

buzzer = Pin(25, Pin.OUT)

while True:
    buzzer.on()
    sleep(0.1)
    buzzer.off()
    sleep(0.1)