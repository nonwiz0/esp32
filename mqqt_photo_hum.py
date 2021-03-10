# Complete project details at https://RandomNerdTutorials.com
import dht
from utime import sleep
import time
from umqttsimple import MQTTClient
import ubinascii
import machine
import micropython
import network
import esp
esp.osdebug(None)
import gc
gc.collect()

dht = dht.DHT11(Pin(14, Pin.IN))
photo_r = ADC(Pin(35))
photo_r.atten(ADC.ATTN_11DB)

ssid = 'AIU-WIFI'
password = ''
mqtt_server = '10.0.2.101'
#EXAMPLE IP ADDRESS
#mqtt_server = '192.168.1.144'
client_id = ubinascii.hexlify(machine.unique_id())
topic_sub = b'air_quality'
topic_pub = b'dht'

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
    print("Client", client);
except OSError as e:
    restart_and_reconnect()

while True:
    try:
        client.check_msg()
        if (time.time() - last_message) > message_interval:
            d.measure()
            temp = d.temperature()
            hum = d.humidity()
            msg = b'Hello #{}, Temp: {}°C, Hum: {}g.kg^-1'.format(counter, temp, hum)
            print('Sending message: {}'.format(msg))
            client.publish(topic_pub, msg)
            last_message = time.time()
            counter += 1
    except OSError as e:
        restart_and_reconnect()


