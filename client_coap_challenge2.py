# Paula Andreas Broset Bryan
# COAP Challenge 2
import network
import machine
import microcoapy
from time import sleep
from machine import Pin
import dht


wlan = network.WLAN(network.STA_IF)
wlan.active(True)
d = dht.DHT11(Pin(27, Pin.IN))
buzzer = Pin(25, Pin.OUT)

_MY_SSID = 'AIU-WIFI'
_MY_PASS = ''
_SERVER_IP = '10.0.12.254'
# I am connecting to Andreas Server node here, for now we jus wanna see can we turn on the led or not
_SERVER_PORT = 5683  # default CoAP port
_COAP_POST_URL = 'dht/getValue'


def connectToWiFi():
    nets = wlan.scan()
    for net in nets:
        ssid = net[0].decode("utf-8")
        if ssid == _MY_SSID:
            print('Network found!')
            wlan.connect(ssid, _MY_PASS)
            while not wlan.isconnected():
                machine.idle()  # save power while waiting
            print('WLAN connection succeeded!')
            break

    return wlan.isconnected()


def sendPostRequest(client, message):
     # About to post message...
    messageId = client.post(_SERVER_IP, _SERVER_PORT, _COAP_POST_URL, message,
                                    None, microcoapy.COAP_CONTENT_FORMAT.COAP_TEXT_PLAIN)
    print("[POST] Message Id: ", messageId)
     # wait for response to our request for 2 seconds
    client.poll(10000)
    
def receivedMessageCallback(packet, sender):
    print('Message received:', packet.toString(), ', from: ', sender)
    
    
connectToWiFi()

client = microcoapy.Coap()
client.discardRetransmissions = True
#client.debug = False
# setup callback for incoming response to a request
client.responseCallback = receivedMessageCallback

# Starting CoAP...
client.start()

# sendPostRequest(client)
# sendPutRequest(client)


while True:
    # Checking the temperature
    d.measure()
    temp = d.temperature()
    humi = d.humidity()
    message = "Node{} Nn Temp: {} Celcius Tn Humidity: {} Humid".format(1, temp, humi)
    print("Sending {} to the Coap_Server".format(message))
    if temp > 27:
        buzzer.on()
        sleep(1)
        buzzer.off()
    sleep(.5)
    sendPostRequest(client, message)
   
    
# stop CoAP
client.stop()
