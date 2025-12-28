import network
import time

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

while True:
    print("Envoi de START à ESP A...")
    e.send(peer_mac, b"START")
    print("START envoyé !")

    print("Réception des OK...")
    nbr_ok = 0
    while nbr_ok < 10:
        host, msg = e.recv()
        nbr_ok += 1
        print("OK reçu:", nbr_ok, "/ 10")
    else:
        print("Timeout ou message inconnu")

    print("Réception terminée !")
