import network
import espnow
import time
import random
from mac_addr import *

# Initialisation Wi-Fi en mode station
sta = network.WLAN(network.STA_IF)
sta.active(True)

# Initialisation ESP-NOW
e = espnow.ESPNow()
e.active(True)


# Ajouter le pair
mac = telecommande_mac[1]
e.add_peer(mac)

while True:
    pid = random.randint(1, 7)
    vit = random.randint(0, 2)
    msg = f"PID={pid},{vit}"

    e.send(mac, msg)
    print("Message envoyé :", mac, msg)
    time.sleep(3)  # Attendre 1 seconde


