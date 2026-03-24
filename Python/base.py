import network
import time
from mac_addresses import *

MAC = network.WLAN().config("mac")

robot_mac = {
    1 : b'H\xf6\xeez/\xd4',
    2 : b'H\xf6\xeez0(',
    3 : b'',
    4 : b'',
    5 : b'',
    6 : b'',
    7 : b''
    }

# Initialisation du WiFi en mode station (requis pour ESP-NOW)
w0 = network.WLAN(network.STA_IF)
w0.active(True)

while True:
    mac = w0.config('mac')
    if mac and mac != b'\x00\x00\x00\x00\x00\x00':
        break
    time.sleep_ms(10)

print("WiFi prêt, MAC :", MAC)

import espnow

# Initialisation d’ESP-NOW
e = espnow.ESPNow()
e.active(True)

# Adresse MAC de ESP B
peer_mac = robot_mac[1]
peer_mac = MACB

e.add_peer(peer_mac)

print("Base prêt et attend Robot...", peer_mac)

def irq(e):
    host, msg = e.recv()
    if msg:
        print("Reçu :", msg, "de", host)

e.irq(irq)

while True:
    print("waiting...")
    time.sleep(5)
