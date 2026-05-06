import network
import espnow
import time

# -----------------------
# Initialisation WiFi + ESP-NOW
# -----------------------
w = network.WLAN(network.STA_IF)
w.active(True)

e = espnow.ESPNow()
e.active(True)

broadcast = b'\xff\xff\xff\xff\xff\xff'

# Ajouter le broadcast comme peer
try:
    e.add_peer(broadcast)
except OSError:
    pass

mac_base = None

# -----------------------
# Callback de réception
# -----------------------
def on_recv(_):
    global mac_base
    while True:
        host, msg = e.irecv(0)
        if not host:
            break

        print("Reçu de", host, ":", msg)

        # base répond avec "MASTER=<MAC>"
        if msg.startswith(b"MASTER="):
            mac_base = msg.split(b"=")[1]
            print("MAC de base détecté :", mac_base)

            # Ajouter base comme peer
            try:
                e.add_peer(mac_base)
            except OSError:
                pass

            # Envoyer un message de confirmation
            e.send(mac_base, b"READY")
            print("Message READY envoyé à base")

e.irq(on_recv)

# -----------------------
# Envoi du broadcast de découverte
# -----------------------
print("Envoi du broadcast HELLO...")
e.send(broadcast, b"HELLO")

# -----------------------
# Boucle principale
# -----------------------
while True:
    time.sleep(1)
