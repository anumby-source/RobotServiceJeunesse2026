###################################################################
#
#   RSJ2026 : Robot code
#
###################################################################

import network
import espnow
from time import sleep_ms, ticks_ms
from machine import Pin, UART
from dcMotor import dcMotor
from mac_addr import *

#
num, _ = find_robot()
robotAddr = robot_mac[num]
telecommandeAddr = telecommande_mac[num]

# motors initialization
ml = dcMotor(pin1=11, pin2=12, pinEn=9)      # left motor
mr = dcMotor(pin1=7, pin2=3, pinEn=5)        # right motor
ml.duty_offset = 0
mr.duty_offset = 0
print("robot : motor init ok")

# led initialization
led = Pin(15, Pin.OUT)
led.off()     # led on
sleep_ms(1000)
led.on()      # led off
print("robot : led init ok")

# UART initialization
u = UART(0, rx=Pin(14, Pin.IN), tx=Pin(13, Pin.OUT))
print("robot : UART init ok")

# espnow initialization
sta = network.WLAN(network.STA_IF) # A WLAN interface must be active
sta.active(True)
sta.disconnect()   # Because ESP8266 auto-connects to last Access Point
print("robot : WLAN init ok")
e = espnow.ESPNow()
e.active(True)
print("robot : espnow init ok")

# add telecommande and base to peers
try:
    e.add_peer(telecommandeAddr)
except:
    pass         # if telecommande already in peer list
print(b"robot : telecommande address added")
# 
try:
    e.add_peer(baseAddr)
except:
    pass         # if baseAddr already in peer list
print(b"robot : base address added")
#

u.read(u.any())   # empty uart buffer
msg = b''
#
while True:
    if u.any():
        msg += u.read(u.any())
        if msg[-1] == 0x0a:  # last char = '\n'
            e.send(baseAddr, msg)
            print(msg)
            e.send(telecommandeAddr, msg)
            msg = b''       
    try:
        addr, cmd = e.recv(0)
        if cmd: print(cmd)
        if addr == telecommandeAddr:
            exec(cmd)
    except:
        if cmd: print(b"robot : error command:" + cmd)
        led.off()    # led on
        break