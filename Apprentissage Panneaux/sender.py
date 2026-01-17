from machine import UART
import time
import random

uart = UART(1, baudrate=9600, tx=5, rx=6)

# on suppose le nombre d'images
images = 12


# on crée un message qui contient l'identifiant de l'image à capturer
def build_msg(N):
    if not (1 <= N <= images):
        raise ValueError(f"N doit être entre 1 et {images}")
    return "{:02d}".format(N).encode()


# ici simule l'action de capturer une image choisie au hasard:
#   le message est envoyé au k210 et on souppose que l'on a visualisé
#   une image donnée.
#   en envoyant un identifiant, l'image est donc capturée et associée
#   avec cet identifiant.

i = 0
while True:
    i += 1
    message = b'message from ESP32 #' + f"{i}"
    r = random.randint(0, images)
    if r > 0:
        message = build_msg(r)
    n = uart.write(message)

    print(time.time(), "sent", message, n)
    time.sleep(1)

