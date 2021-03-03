# Andreas Christian Mambu and Chanbroset Prach
from machine import Pin
from utime import sleep

buzzer = Pin(32, Pin.OUT)

while True:
    buzzer.on()
    sleep(1)
    buzzer.off()
    sleep(1)