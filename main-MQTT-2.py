# Complete project details at https://RandomNerdTutorials.com

import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import micropython
import network
import esp
esp.osdebug(None)
import gc
gc.collect()

ssid = 'YOUR-WIFI-HERE'
password = 'YOUR-PASSWORD-HERE'
mqtt_server = 'YOUR-IP-SERVER-HERE'
#EXAMPLE IP ADDRESS
#mqtt_server = '192.168.1.144'
client_id = ubinascii.hexlify(machine.unique_id())
topic_sub = b'hello'
topic_pub = b'notification'

last_message = 0
message_interval = 5
counter = 0

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
######################################
######################################

def sub_cb(topic, msg):
    print((topic, msg))
    if topic == b'notification' and msg == b'received':
        print('ESP received hello message')

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
        new_message = client.check_msg()
        if new_message != None:
            client.publish(topic_pub, b'received')
        time.sleep(1)
    except OSError as e:
        restart_and_reconnect()