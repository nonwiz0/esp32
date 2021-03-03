from machine import Pin
from time import sleep
btn = Pin(35, Pin.IN, Pin.PULL_UP)
while True:
    print(btn.value())
    sleep(1)