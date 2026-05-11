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

# Liste des clients déjà connus
clients = set()

mac_base = w.config('mac')
print("MAC de base :", mac_base)

# -----------------------
# Callback de réception
# -----------------------
def on_recv(_):
    while True:
        host, msg = e.irecv(0)
        if not host:
            break

        print("Reçu de", host, ":", msg)

        # Si un robot envoie "HELLO"
        if msg == b"HELLO":
            if host not in clients:
                print("Nouveau robot détecté :", host)
                clients.add(host)

                # Ajouter robot comme peer
                try:
                    e.add_peer(host)
                except OSError:
                    pass  # déjà ajouté

            # Répondre avec l'adresse MAC de base
            payload = b"MASTER=" + mac_base
            e.send(host, payload)
            print("Réponse envoyée à", host)

e.irq(on_recv)

# -----------------------
# Boucle principale
# -----------------------
print("base prêt. En attente des broadcasts...")
while True:
    time.sleep(1)
