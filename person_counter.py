#Arthur and Rakai
from hcsr04 import HCSR04
from utime import sleep
from machine import Pin, PWM
import random

def beep(num):
    for loop in range(num):
        passive_buzzer = PWM(Pin(26, Pin.OUT), freq=random.randrange(200, 400), duty=512)
        sleep(0.15)
        passive_buzzer.deinit()
        sleep(0.02)


s1 = HCSR04(12, 14)

while True:

    dist_s1 = s1.distance_cm()
    print("No person detected")
    if dist_s1 < 20:
        beep(7)
        print("A Person detected","at distance:",dist_s1)

    while True:

        dist_s1 = s1.distance_cm()

        if dist_s1 < 20:
            beep(1)
            print("Person is still standing","At distance",dist_s1)
        else:
            break
    sleep(0.5)
   


