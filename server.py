import usocket as socket
from machine import Pin
import network
import esp
import gc
import dht

# Create sensor DHT object
d = dht.DHT11(Pin(32, Pin.IN))

ssid = 'Nagato'
password = 'Asd,car15'

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
    pass
print('Connection successfully')
print(station.ifconfig())
led = Pin(2, Pin.OUT)

def web_page():
    print("LED value: ", led.value())
    if led.value() == 1:
        gpio_state = "ON"
    else:
        gpio_state = "OFF"
    html = """<html>
     <head>
     <title>ESP Web Server</title>
     <meta http-equiv="refresh" content="1">
     <meta name="viewport" content="width=device-width, initial-scale=1">
     <link rel="icon" href="data:,"> <style>html{font-family: Helvetica;
    display:inline-block; margin: 0px auto; text-align: center;}
     h1{color: #0F3376; padding: 2vh;}p{font-size: 1.5rem;}.button{display:
    inline-block; background-color: #e7bd3b; border: none;
     border-radius: 4px; color: white; padding: 16px 40px; text-decoration:
    none; font-size: 30px; margin: 2px; cursor: pointer;}
     .button2{background-color: #4286f4;}</style>
     </head>
     <body>
    
    <h1>ESP Web Server</h1>
    <p> Temperature: """ + str(temp) + """ °C </p>
    <p> Humidity: """ + str(hum) + """ g.kg^-1 </p>
    <p>GPIO state: <strong>""" + gpio_state + """</strong></p>
    
     <p><a href="/?led=on"><button class="button">ON</button></a></p>
     <p><a href="/?led=off"><button class="button button2"> OFF
    </button></a></p>
     </body>
    </html> """
    return html
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
    conn, addr = s.accept()
    print(' Got a connection from {}'.format(str(addr)))
    request = conn.recv(1024)
    request = str(request)
    print('Content = {}'.format(request))
    led_on = request.find('/?led=on')
    led_off = request.find('/?led=off')
    d.measure()
    temp = d.temperature()
    hum = d.humidity()
    if temp >= 29:
        led.value(1)
    else:
        led.value(0)
    if led_on == 6:
        print('LED ON')
        led.value(1)
    else:
        if led_off == 6:
            print('LED OFF')
            led.value(0)
    response = web_page()
    
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()
        
