import network
import time

time.sleep(0.3)

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

print("Envoi de START à ESP A...")
e.send(peer_mac, b"START")
print("START envoyé !")

print("Réception des OK...")
while True:
    host, msg = e.recv()
    if msg:
        print("Reçu :", msg, "de", host)

