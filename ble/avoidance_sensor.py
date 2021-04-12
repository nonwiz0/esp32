from machine import Pin
from time import sleep
sensor = Pin(32,Pin.IN,Pin.PULL_UP)
while True:
    print(sensor.value())
    sleep(1)