# Chanbroset Prach and Andreas Christian

from hcsr04 import HCSR04
from utime import sleep_ms
from machine import Pin

curr_person = 0
s2 = HCSR04(27, 26)
s1 = HCSR04(32, 33)

q0, q1, q2, qEnt, qExt = 0, 1, 2, 3, 4
m = [
    # S1 S2 E
    [q1, q2, q0], # q0
    [q1, qEnt, q0], # q1
    [qExt, q2, q0], # q2
    [q1, qEnt, q0], # qEnt
    [qExt, q2, q0], # qExt
    ]
state = q0

def detect():
    '''
        S1 active: return 0
        s2 active: return 1
        s1 and s2 active: return 2
        empty: return 2
    '''
    sd1 = s1.distance_cm()
    sd2 = s2.distance_cm()
    print("The distance from sensor 1 is ", sd1, " cm")
    print("The distance from sensor 2 is ", sd2, " cm")
    ans = 2
    threshold = 10
    if sd1 < threshold and sd2 < threshold:
        ans = 2
    elif sd1 < threshold:
        ans = 0
    elif sd2 < threshold:
        ans = 1
    return ans

while True:
    x = detect()
    state = m[state][x]
    if state == qEnt:
        curr_person += 1
    elif state == qExt:
        curr_person -= 1
    print("The person inside the room is ", curr_person)
    sleep_ms(500)



# while True:
#     dist_s1 = s1.distance_cm()
#     dist_s2 = s2.distance_cm()
#     counter = 0
#     if dist_s1 < 10:
#         counter += 1
#     if dist_s2 < 10 and counter == 1:
#         sleep_ms(500)
#         curr_person += 1       
#     
#     if dist_s2 < 10:
#         counter -= 1
#     if dist_s1 < 10 and counter == -1:
#         sleep_ms(500)
#         curr_person -= 1
#         
#     
#     print("The distance from sensor 1 is ", dist_s1, " cm")
#     print("The distance from sensor 2 is ", dist_s2, " cm")
#     print("The person inside the room is ", curr_person)
#     sleep_ms(100)