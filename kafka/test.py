from random import randint
from time import sleep

v1 = randint(0,100)

while True:
    print(v1)
    d = randint(-1,1)
    v1 = v1 + d
    sleep(0.25)
