#Chanbroset, Andreas, Bryan
from umqtt.robust import MQTTClient
import machine as m
import ubinascii
import network
import time
import dht
from machine import Pin
from time import sleep

sta_if = network.WLAN(network.STA_IF); sta_if.active(True)
sta_if.scan() # Scan for available access points
sta_if.active(True)
sta_if.connect("AIU-WIFI", "") # Connect to an AP
sta_if.isconnected()
time.sleep(3)

ubidotsToken = "BBFF-SPONj6AlHG36Okio1VdmISf9jX55G2"
clientID = ubinascii.hexlify(m.unique_id())
client = MQTTClient("clientID", "industrial.api.ubidots.com", 1883, user = ubidotsToken, password = ubidotsToken)


def checkwifi():
    while not sta_if.isconnected():
        time.sleep_ms(500)
        print("Connecting WiFI failed")
        sta_if.connect()

pin13 = m.Pin(13, m.Pin.IN, m.Pin.PULL_UP)
d = dht.DHT11(Pin(32, Pin.IN))

def publish():
    hum = 0
    temp = 0
    while True:
        checkwifi()
        client.connect()
        d.measure()
        temp = d.temperature()
#         print("Temperature: ", temp, "°C")
        hum = d.humidity()
#         print("Humidity: ", hum, "g.kg^-1")
        sleep(1)
        msg = b'{"temp":%s, "hum":%s, "dht": {"context":{"hum": %s, "temp": %s}}}' % (temp, hum, hum, temp)
        print(msg)
        client.publish(b"/v1.6/devices/ESP32", msg)
        time.sleep(10)

publish()

