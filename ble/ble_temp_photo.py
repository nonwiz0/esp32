# Bryan, Broset, Paula, Andreas
from machine import Pin, Timer
from time import sleep_ms
import ubluetooth
from machine import Pin, ADC
from time import sleep
import dht
p = ADC(Pin(35))
p.atten(ADC.ATTN_11DB)
d = dht.DHT11(Pin(32, Pin.IN))
class BLE():
    def __init__(self, name):   
        self.name = name
        self.ble = ubluetooth.BLE()
        self.ble.active(True)
        
        self.led = Pin(2, Pin.OUT)
        self.timer1 = Timer(0)
        self.timer2 = Timer(1)
        
        self.disconnected()
        self.ble.irq(self.ble_irq)
        self.register()
        self.advertiser()

    def connected(self):        
        self.timer1.deinit()
        self.timer2.deinit()

    def disconnected(self):        
        self.timer1.init(period=1000, mode=Timer.PERIODIC, callback=lambda t: self.led(1))
        sleep_ms(200)
        self.timer2.init(period=1000, mode=Timer.PERIODIC, callback=lambda t: self.led(0))   

    def ble_irq(self, event, data):
        print(self, event, data)
        if event == 1:
            '''Central disconnected'''
            self.connected()
            self.led(1)
        
        elif event == 2:
            '''Central disconnected'''
            self.advertiser()
            self.disconnected()
        
        elif event == 3:
            '''New message received'''            
            buffer = self.ble.gatts_read(self.rx)
            message = buffer.decode('UTF-8').strip()
            d.measure()
            temp = str(d.temperature())
            print(temp)
            ble.send("Temp: "+temp+" °C")
            print(message)
        else:
            d.measure()
            temp = str(d.temperature())
            print(temp)
            ble.send("Temp: "+temp+" °C") 
           
    def register(self):        
        # Nordic UART Service (NUS)
#         NUS_UUID = '6E400001-B5A3-F393-E0A9-E50E24DCCA9E'
#         RX_UUID = '6E400002-B5A3-F393-E0A9-E50E24DCCA9E'
#         TX_UUID = '6E400003-B5A3-F393-E0A9-E50E24DCCA9E'
#
        # Environmental Sensing
        TMP_UUID = '0000181A-0000-1000-8000-00805F9B34FB'
        TM_UUID = '00002ABE-0000-1000-8000-00805F9B34FB'
        
        # Photo resistor
        PHR_UUID = '00001802-0000-1000-8000-00805F9B34FB'
        PH_UUID = '00002ABE-0000-1000-8000-00805F9B34FB'
        
        BLE_TMP = ubluetooth.UUID(TMP_UUID)
        BLE_TM = (ubluetooth.UUID(TM_UUID), ubluetooth.FLAG_NOTIFY)
         
        BLE_PHR = ubluetooth.UUID(PHR_UUID)
        BLE_PH = (ubluetooth.UUID(PH_UUID), ubluetooth.FLAG_NOTIFY)
        
#         BLE_NUS = ubluetooth.UUID(NUS_UUID)
#         BLE_RX = (ubluetooth.UUID(RX_UUID), ubluetooth.FLAG_WRITE)
#         BLE_TX = (ubluetooth.UUID(TX_UUID), ubluetooth.FLAG_NOTIFY)
#         
        BLE_TMP_UART = (BLE_TMP, (BLE_TM,))
        BLE_PHR_UART = (BLE_PHR, (BLE_PH,))
       # BLE_UART = (BLE_NUS, (BLE_TX, BLE_RX,))
        #SERVICES = (BLE_UART, BLE_TMP_UART, BLE_PHR_UART,)
        SERVICES = (BLE_TMP_UART, BLE_PHR_UART,)
       # ((self.tx, self.rx,), (self.tm,), (self.ph,) ) = self.ble.gatts_register_services(SERVICES)
        ((self.tm,), (self.ph,) ) = self.ble.gatts_register_services(SERVICES)

    def send(self, data):
        self.ble.gatts_notify(0, self.tm, data + '\n')

    def sendPH(self, data):
        self.ble.gatts_notify(0, self.ph, data + '\n')
        
    def advertiser(self):
        name = bytes(self.name, 'UTF-8')
        self.ble.gap_advertise(100, bytearray('\x02\x01\x02') + bytearray((len(name) + 1, 0x09)) + name)
        
ble = BLE("Hum_Lum_Reporter")
i = 0

while True:
    sleep_ms(1000)
    d.measure()
    humidity = str(d.humidity())
    i = (i + 1) % 101
    # It'll report every 2 seconds, cna increase if encounter error
    # 5 sec works as well
    if i % 2 == 0:
        ble.send("Hum: "+humidity+" g.kg^-1")
        if p.read() > 2000:
            ble.sendPH("Darker: "+str(p.read())+" unit")
        else:
            ble.sendPH("Lighter: "+str(p.read())+" unit")
# [Errno 107] ENOTCONN
# If You get this error, please restart the device
# Or increase the notification duration
    
