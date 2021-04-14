# Andreas, Broset, Paula, Bryan
# Our Group code name is ABPNB001
import ubluetooth as bluetooth
import struct
import time
from ble_advertising import advertising_payload
from machine import Pin
from time import sleep
import dht

d = dht.DHT11(Pin(32, Pin.IN))

from micropython import const
_IRQ_CENTRAL_CONNECT                 = const(1 << 0)
_IRQ_CENTRAL_DISCONNECT              = const(1 << 1)

_BATTERY_UUID = bluetooth.UUID(0x181A)
_BATTERY_LEVEL_CHAR = (bluetooth.UUID(0x2ABE), bluetooth.FLAG_READ|bluetooth.FLAG_NOTIFY,)
_BATTERY_SERVICE = (_BATTERY_UUID, (_BATTERY_LEVEL_CHAR,),)
# You can see here we're using battery
class BLEBattery:
    def __init__(self, ble, name='Temperature Reporting'):
        self._ble = ble
        self._ble.active(True)
        self._ble.irq(handler=self._irq)
        ((self._handle,),) = self._ble.gatts_register_services((_BATTERY_SERVICE,))
        self._connections = set()
        self._payload = advertising_payload(name=name, services=[_BATTERY_UUID])
        self._advertise()

    def _irq(self, event, data):
        # Track connections so we can send notifications.
        if event == _IRQ_CENTRAL_CONNECT:
            conn_handle, _, _, = data
            self._connections.add(conn_handle)
        elif event == _IRQ_CENTRAL_DISCONNECT:
            conn_handle, _, _, = data
            self._connections.remove(conn_handle)
            # Start advertising again to allow a new connection.
            self._advertise()

    def set_level(self, level_percentage, notify=False):
        print(level_percentage)
        #self._ble.gatts_notify(conn_handle, str(level_percentage) + '\n')
        # Write the local value, ready for a central to read.
        self._ble.gatts_write(self._handle, struct.pack('=10s', str(level_percentage)+" g.kg^-1"))
        print("Level percentage", level_percentage)
        if notify:
            for conn_handle in self._connections:
                # Notify connected centrals to issue a read.
                self._ble.gatts_notify(conn_handle, self._handle)

    def _advertise(self, interval_us=500000):
        self._ble.gap_advertise(interval_us, adv_data=self._payload)


def demo():
    ble = bluetooth.BLE()
    batt = BLEBattery(ble)

    i = 25

    while True:
        # Write every second, notify every 10 seconds.
        i = (i + 1) % 101
        d.measure()
        batt.set_level(d.humidity(), notify=(i % 2 == 0))
        time.sleep_ms(1000)


if __name__ == '__main__':
    demo()
