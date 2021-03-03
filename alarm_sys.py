
from machine import Pin
from time import sleep

buzzer = Pin(32, Pin.OUT)
btn = Pin(35, Pin.IN, Pin.PULL_UP)
led = Pin(2, Pin.OUT)

while True:
    print(btn.value())
    if btn.value() == 0:
        buzzer.on()
        led.value(1)
        sleep(.5)
        led.value(0)
    else:
        buzzer.off()
    sleep(1)



