# Andreas, Broset, Bryan, Paula

import network
import machine
import microcoapy
import utime as time
from utime import sleep
import random
from machine import Pin, PWM
import dht

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
buzzer = Pin(25, Pin.OUT)
_MY_SSID = 'AIU-WIFI'
_MY_PASS = ''
_SERVER_PORT = 5683  # default CoAP port
d = dht.DHT11(Pin(32, Pin.IN))
led = Pin(2, Pin.OUT)

def connectToWiFi():
    print('Starting attempt to connect to the WiFi...')
    nets = wlan.scan()
    for net in nets:
        ssid = net[0].decode("utf-8")
        if ssid == _MY_SSID:
            print('Network found!')
            wlan.connect(ssid, _MY_PASS)
            while not wlan.isconnected():
                machine.idle()  # save power while waiting

            connectionResults = wlan.ifconfig()
            print('WLAN connection succeeded with IP: ', connectionResults[0])
            break

    return wlan.isconnected()

connectToWiFi()

def getDHT(packet, senderIp, senderPort):
    d.measure()
    temp = str(d.temperature()) + " deg celsius"
    hum = str(d.humidity()) + "g.kg^-1"
    message = temp + ", " + hum
    client.sendResponse(senderIp, senderPort, packet.messageid, message, microcoapy.COAP_RESPONSE_CODE.COAP_CONTENT, microcoapy.COAP_CONTENT_FORMAT.COAP_NONE, packet.token)
   

def turnOnLed(packet, senderIp, senderPort):
    led.value(1) 
    print('Turn-on-led request received:', packet.toString(), ', from: ', senderIp, ":", senderPort)
    
def turnOffLed(packet, senderIp, senderPort):
    led.value(0) 
    print('Turn-off-led request received:', packet.toString(), ', from: ', senderIp, ":", senderPort)
    

def playBuzzer(packet, senderIp, senderPort):
    print('Play Buzzer request received:', packet.toString(), ', from: ', senderIp, ":", senderPort)
    l = 0
    passive_buzzer = PWM(buzzer, freq=random.randrange(200, 400), duty=512)
    while l < 10:
        passive_buzzer = PWM(buzzer, freq=random.randrange(200, 400), duty=512)
        sleep(0.2)
        l += 1
    passive_buzzer.deinit()
  
    
client = microcoapy.Coap()
# setup callback for incoming response to a request
client.addIncomingRequestCallback('led/turnOn', turnOnLed)
client.addIncomingRequestCallback('led/turnOff', turnOffLed)
client.addIncomingRequestCallback('buzz/play', playBuzzer)
client.addIncomingRequestCallback('dht/getValue', getDHT)
# client.addIncomingRequestCallback('buzz/stop', stopBuzzer)

# Starting CoAP...
client.start()

# wait for incoming request for 60 seconds
timeoutMs = 60000
start_time = time.ticks_ms()
while time.ticks_diff(time.ticks_ms(), start_time) < timeoutMs:
    client.poll(60000)

# stop CoAP
client.stop()

