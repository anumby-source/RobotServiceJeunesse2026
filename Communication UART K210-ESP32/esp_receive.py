from machine import Pin, UART
import time
import network
import espnow
from mac_addr import *

num = 1
robotAddr = robot_mac[num]
telecommandeAddr = telecommande_mac[num]

print("MAC=", robot_mac[num])
print("Base=", baseAddr)

# espnow initialization
sta = network.WLAN(network.STA_IF) # A WLAN interface must be active
sta.active(True)
sta.disconnect()   # Because ESP8266 auto-connects to last Access Point
print("robot : WLAN init ok")
e = espnow.ESPNow()
e.active(True)
print("robot : espnow init ok")


try:
    e.add_peer(telecommandeAddr)
except:
    pass         # if telecommande already in peer list
print(b"robot : telecommande address added")

# setup UART

# ESP32-C3 Super Mini
uart = UART(1, baudrate=115200, tx=5, rx=6)
#uart = UART(0, rx=Pin(14, Pin.IN), tx=Pin(13, Pin.OUT), baudrate=9600)

# loop
msg = b''
while True:
    if uart.any():
        msg += uart.read(uart.any())
        if msg[-1] == 0x0a: 
            e.send(telecommandeAddr, msg[:-1])
            print("line", msg)
            msg = b''
