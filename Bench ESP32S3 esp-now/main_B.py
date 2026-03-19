import network
import time
import os
import random
from mac_addresses import *

# Mode station obligatoire
w0 = network.WLAN(network.STA_IF)
w0.active(True)

# Attendre que MAC ≠ 00:00:00:00:00:00
while True:
    mac = w0.config('mac')
    if mac and mac != b'\x00\x00\x00\x00\x00\x00':
        break
    time.sleep_ms(10)

print("WiFi prêt, MAC :", mac)

import espnow

# Initialisation ESP-NOW
e = espnow.ESPNow()
e.active(True)

# Adresse MAC de ESP A
peer_mac = MACA

e.add_peer(peer_mac)

try:
    while True:
        print("Envoi de START à ESP A...")
        e.send(peer_mac, b"START")
        print("START envoyé !")

        print("Réception des OK...")
        for nbr_ok in range(11):
            print("attente...")
            host, msg = e.recv(10000)
            if msg is not None:
                print("OK reçu:", nbr_ok + 1, "/ 10", "msg=", msg[0:4], "len=", len(msg))
            else:
                print("Timeout ou message inconnu")

        print("Réception terminée !")

except KeyboardInterrupt:
    print("Ctrl-C capturé : arrêt propre.")
    e.active(False)
    w0.active(False)

