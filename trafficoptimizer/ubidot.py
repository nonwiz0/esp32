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
sta_if.connect("ELIJAH-WIFI", "") # Connect to an AP
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


def publish():
    zzzz = 25
    while True:
        checkwifi()
        client.connect()
        zzzz = (zzzz + 4) % 50
        if zzzz < 20:
            zzzz += 20
        print("zzzzerature: ", zzzz, "°C")
        sleep(1)
        msg = b'{"zzzz":%s, "str":%s}' % (zzzz, b'asdf')
        print(msg)
        client.publish(b"/v1.6/devices/ESP32", msg)
        time.sleep(10)

publish()

