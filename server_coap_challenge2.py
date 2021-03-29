# Andreas, Broset, Bryan, Paula
from umqtt.robust import MQTTClient
import machine as m
import ubinascii
import dht
from machine import Pin
from time import sleep
import time
import network
import microcoapy
import random
from machine import Pin, PWM
import dht

ubidotsToken = "BBFF-SPONj6AlHG36Okio1VdmISf9jX55G2"
clientID = ubinascii.hexlify(m.unique_id())
ubi_client = MQTTClient("clientID", "industrial.api.ubidots.com", 1883, user = ubidotsToken, password = ubidotsToken)
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
buzzer = Pin(25, Pin.OUT)

_MY_SSID = 'AIU-WIFI'
_MY_PASS = ''
_SERVER_PORT = 5683  # default CoAP port
d = dht.DHT11(Pin(32, Pin.IN))
led = Pin(2, Pin.OUT)

def publish(node, temp, hum):
    ubi_client.connect()
    sleep(1)
    msg = b'{"node:":%s, "coap_temp":%s, "coap_hum":%s}' % (node, temp, hum)
    print("Uploading", msg, "to ubidot")
    ubi_client.publish(b"/v1.6/devices/ESP32", msg)
    time.sleep(10)

def connectToWiFi():
    print('Starting attempt to connecto to WiFi...')
    nets = wlan.scan()
    for net in nets:
        ssid = net[0].decode("utf-8")
        if ssid == _MY_SSID:
            print('Network found!')
            wlan.connect(ssid, _MY_PASS)
            while not wlan.isconnected():
                m.idle()  # save power while waiting

            connectionResults = wlan.ifconfig()
            print('WLAN connection succeeded with IP: ', connectionResults[0])
            break

    return wlan.isconnected()

connectToWiFi()

 

def getDHT(packet, senderIp, senderPort):
    print('DHT request received:', packet.toString(), ', from: ', senderIp, ":", senderPort)
    print("packet payload: {}".format(packet.payload))
    message = packet.payload.decode()
    node_num = int(message[message.find('e') + 1 : message.find(' Nn')])
    temp = message[message.find(': ')+2 : message.find(' Tn')]
    hum = message[message.find('y: ')+3: len(message)]
    print("Node: {}\nTemp: {}\nHum: {}".format(node_num, temp, hum))
    for i in range(node_num):
        buzzer.on()
        sleep(1)
        buzzer.off()
    publish(node_num, temp, hum)
    
    
client = microcoapy.Coap()
# setup callback for incoming response to a request
client.addIncomingRequestCallback('dht/getValue', getDHT)

# Starting CoAP...
client.start()

# wait for incoming request for 60 seconds
timeoutMs = 60000
start_time = time.ticks_ms()
while time.ticks_diff(time.ticks_ms(), start_time) < timeoutMs:
    client.poll(60000)

# stop CoAP
client.stop()

