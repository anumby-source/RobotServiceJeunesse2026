import network
import time

# Initialisation du WiFi en mode station (requis pour ESP-NOW)
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

# Initialisation d’ESP-NOW
e = espnow.ESPNow()
e.active(True)

# Adresse MAC de ESP B
peer_mac = MACB

e.add_peer(peer_mac)

print("ESP A prêt et attend START...")

while True:
    host, msg = e.recv()
    if msg:
        print("Reçu :", msg, "de", host)
        if msg == b"START":
            print("START reçu, j’envoie 10 fois OK...")
            for i in range(10):
                e.send(peer_mac, b"OK")
                print("OK envoyé", i+1)
                time.sleep(0.2)

