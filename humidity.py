# Chanbroset Prach n Andreas Christian
import dht
from machine import Pin
from time import sleep

# Create sensor DHT object
d = dht.DHT11(Pin(32, Pin.IN))

while True:
    d.measure()
    temp = d.temperature()
    print("Temperature: ", temp, "°C")
    hum = d.humidity()
    print("Humidity: ", hum, "g.kg^-1")
    sleep(1)
    
    