import network
import espnow
import time
from mac_addr import *

# Initialisation Wi-Fi en mode station
sta = network.WLAN(network.STA_IF)
sta.active(True)

# Initialisation ESP-NOW
e = espnow.ESPNow()
e.active(True)

# Afficher l'adresse MAC de cet ESP32 (pour la configurer dans l'émetteur)
print("Adresse MAC de cet ESP32 :", sta.config('mac'))

def callback(e):
        # Attendre un message
        mac, msg = e.recv()
        if msg:  # Si un message est reçu
            print("Message reçu :", msg.decode('utf-8'))

# Configurer le callback pour recevoir les messages
e.irq(callback)

while True:
    time.sleep(1)