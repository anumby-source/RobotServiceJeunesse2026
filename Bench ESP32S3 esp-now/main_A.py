import network
import time
import os
import random

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


def build_msg(seq):
    # seq = numéro d’ordre

    # Taille aléatoire entre 1 et 200 bytes
    plen = random.randint(1, 200)

    # Génération du payload
    payload = os.urandom(plen)

    # Construction du message
    msg = bytearray()
    msg.extend(b"OK")
    msg.extend(seq.to_bytes(2, "big"))  # 2 bytes ordonnés
    msg.extend(payload)

    return msg


def irq(e):
    host, msg = e.recv()
    if msg:
        print("Reçu :", msg, "de", host)
        if msg == b"START":
            print("START reçu, j’envoie 10 fois OK...")
            for i in range(11):
                m = build_msg(i + 1)
                e.send(peer_mac, m)
                print("OK envoyé", i + 1, "len=", len(m), "m=", m[0:4])
                # time.sleep(0.2)


e.irq(irq)

m = build_msg(12)
print("M", 12, "len=", len(m), "m=", m[0:4])

while True:
    print("waiting...")
    time.sleep(1)

