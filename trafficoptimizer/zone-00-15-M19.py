import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import micropython
import network
import esp
esp.osdebug(None)
import gc
import random
from main_RGB_LED import RGBLed
from hcsr04 import HCSR04

gc.collect()

ssid = 'ELIJAH-WIFI'
password = ''
mqtt_server = '172.21.3.184'
#EXAMPLE IP ADDRESS
#mqtt_server = '192.168.1.144'
client_id = ubinascii.hexlify(machine.unique_id())

topic_sub = b'zone-response'
topic_pub = b'zones'
current_time = 0
last_message = 0
message_interval = 1
counter = 0
zones = ["Z00", "Z15"]


# Red is 26, Green is 25, Blue is 27
tl_z00 = RGBLed(25, 26, 27)
tl_z15 = RGBLed(18, 19, 21)

def switch_light(led, color):
    if color == 'red':
        led.set(255, 0, 0)
    elif color == 'yellow':
        led.set(255, 255, 0)
    elif color == 'green':
        led.set(0, 255, 0)

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

c = 0
while station.isconnected() == False:
    print('Trying to connect {}'.format(c))
    c += 1
    time.sleep(0.5)
    pass

print('Connection successful')
print(station.ifconfig())
######################################

def sub_cb(topic, msg):
    #print((topic, msg))
    green_light = msg.decode("utf-8")
    green_light = green_light.split("|")
    found_z00 = green_light[0].find(zones[0], 0)
    found_z15 = green_light[0].find(zones[1], 0)
    is_z00_green_light = found_z00 > 0
    is_z15_green_light = found_z15 > 0
    if is_z00_green_light:
        remaining = green_light[0][found_z00 + 5: green_light[0].find(' sec')]
        if int(remaining) < 5:
            switch_light(tl_z00, 'yellow')
        else:
            switch_light(tl_z00, 'green')
            print("Z00 Green Light is on", remaining)
    else:
        switch_light(tl_z00, 'red')
        print("Z00 is Red Light")
        
    if is_z15_green_light:
        #print(is_z15_green_light, green_light[0], green_light[0][found_z15])
        remaining = green_light[0][found_z15 + 5: green_light[0].find(' sec')]
        if int(remaining) < 5:
            switch_light(tl_z15, 'yellow')
        else:
            switch_light(tl_z15, 'green')
        print("Z15 Green Light is on", remaining)
    else:
        print("Z15 is Red Light")
        switch_light(tl_z15, 'red')

def connect_and_subscribe():
    global client_id, mqtt_server, topic_sub
    client = MQTTClient(client_id, mqtt_server)
    client.set_callback(sub_cb)
    client.connect()
    client.subscribe(topic_sub)
    print('Connected to {} MQTT broker, subscribed to {} topic'.format(mqtt_server, topic_sub))
    return client

def restart_and_reconnect():
    print('Failed to connect to MQTT broker. Reconnecting...')
    time.sleep(10)
    machine.reset()

try:
    client = connect_and_subscribe()
except OSError as e:
    restart_and_reconnect()

while True:
    try:
        client.check_msg()
        if (time.time() - last_message) > message_interval:
            s_z00 = HCSR04(trigger_pin=13, echo_pin=12)
            msg = "#{}".format(counter)
            get_z00_dist = s_z00.distance_cm()
            has_vehicle = get_z00_dist < 10
            if has_vehicle:
              has_vehicle = 1
            else:
              has_vehicle = 0
            msg = 'Z00: V{} L0 | Z15: V1 LF'.format(has_vehicle)
            msg = msg.encode()
            client.publish(topic_pub, msg)
            last_message = time.time()
            counter += 1
    except OSError as e:
        restart_and_reconnect()


