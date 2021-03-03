import usocket as socket
from machine import Pin
import network
import esp
import gc
from lib_rgb import RGBLed
from time import sleep

# Define your pin here
PR = 26
PG = 14
PB = 25

rgb = RGBLed(PR, PG, PB)
#        R    G   B
rgb.set(0, 0, 0)

led = Pin(2, Pin.OUT)

ssid = 'ELIJAH-WIFI'
pw = ''

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, pw)

while station.isconnected() == False:
    pass
print('Connection successfully')
print(station.ifconfig())

def web_page(red, green, blue):
    html = """<html>
     <head>
     <title>RGB Controller</title>
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
    
    <h1>RGB Controller</h1>
   
     <form method="GET">
        <div>
            <label for="red"> Red (between 0 and 255): </label>
            <input type="range" name="red" min="0" max="255">
        </div>
        <br />
         <div>
            <label for="green"> Green (between 0 and 255): </label>
            <input type="range" name="green" min="0" max="255">
        </div>
        <br />
         <div>
            <label for="blue"> Blue (between 0 and 255): </label>
            <input type="range" name="blue" min="0" max="255">
        </div>
       <p><button class="button" type="submit">UPDATE</button></p>
        
    </form>
    <h2>
      Current Value
    </h2>
       <p>
         Red: """ + red + """, Green: """ + green + """, Blue: """ + blue + """
       </p>
   
     </body>
    </html> """
    return html
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 81))
s.listen(5)

while True:
    conn, addr = s.accept()
    print(' Got a connection from {}'.format(str(addr)))
    request = conn.recv(1024)
    request = str(request)
   # print('Content = {}'.format(request))
    start = request.find('/?')
    end = request.find('HTTP')
    # print("start :", start, "end: ", end)
    geturl = request[:end]
    print("Get url: ", geturl)
    red = '0'
    blue = '0'
    green = '0'
    if len(geturl) >= 15:
        locategreen = geturl.find('&green')
        red = geturl[geturl.find('=')+1:locategreen]
        if len(red) > 2:
            red = int(geturl[geturl.find('=')+1:locategreen])
        else:
            red = int(0)
        geturl = geturl[locategreen:]
        locateblue = geturl.find('&b')
        green = (geturl[geturl.find('=')+1:locateblue])
        if len(green) > 2:
            green = int(green)
        else:
            green = int(0)
        geturl = geturl[locateblue + 1: len(geturl)]
        blue = geturl[geturl.find('=') + 1: len(geturl)]
        if len(blue) > 2:
            blue = int(blue)
            # print(blue+1)
        else:
            blue = int(0)
        print(red, green, blue)
        rgb.set(red, green, blue)

    print("Request:", request)
    red = str(red)
    green = str(green)
    blue = str(blue)
    response = web_page(red, green, blue)
    
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()
        