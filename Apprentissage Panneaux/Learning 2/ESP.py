from machine import UART
import time
import random
import sys
import re

uart = UART(1, baudrate=115200, tx=5, rx=6)

images = 0


def clear_uart_buffer(uart):
    while uart.any():
        uart.read(uart.any())  # Lit et jette les données restantes
    time.sleep_ms(10)  # Petit délai pour stabiliser


# <IMG:00224,00224,100352,00784>
#     0    1    1    2    2    3
# ....5....0....5....0....5....0
def receive_image():
    # Attente de l'en-tête
    image = 0
    header = None
    PACKET_SIZE = 0
    width = 0
    height = 0
    full_size = 0
    num_packets = 0

    while not header:
        if uart.any():
            header = uart.read(42)
            print("start [", header, "]")
            if header.startswith("<IMG:"):
                print("[", header, "]")
                m = re.match(r"([<]IMG[:])([\d]+)[,]([\d]+)[,]([\d]+)[,]([\d]+)[,]([\d]+)[,]([\d]+)[>].*", header)
                print("m=", m, m.group(1))
                if m.group(1) == b'<IMG:':
                    image = int(m.group(2))
                    PACKET_SIZE = int(m.group(3))
                    width = int(m.group(4))
                    height = int(m.group(5))
                    full_size = int(m.group(6))
                    num_packets = int(m.group(7))

                    print(f"Réception image : {image} {width} x {height}, {full_size} bytes, {num_packets} paquets")

    # Buffer pour l'image
    img_data = bytearray(full_size)
    received_bytes = 0

    # Réception des paquets
    packets = 0
    while received_bytes < full_size:
        if uart.any():
            bytes = min(PACKET_SIZE, full_size - received_bytes)
            data = uart.read(bytes)
            img_data[received_bytes:received_bytes + bytes] = data
            received_bytes += bytes
            packets += 1
            print(f"Reçu bytes={bytes} {received_bytes}/{full_size} packets={packets}")

    print(f"Image reçue ! {image}")

    print("coming data [", uart.any(), "]")

    return img_data, width, height


clear_uart_buffer(uart)

while True:
    # Check for UART data
    if uart.any():
        print(">>> next data", uart.any())
        # Réception et sauvegarde
        print("=========receive_image")
        img_data, width, height = receive_image()
        images += 1
        print("=========image received width=", width, "height=", height, "images=", images)

        """
        # Sauvegarde dans un fichier (optionnel)
        with open('received_image.rgb565', 'wb') as f:
            f.write(img_data)
        print("Image sauvegardée.")
        """

    # Vérifie si des données sont disponibles sur le REPL (clavier)
    # Utilise un try/except pour éviter les blocages
    try:
        if sys.stdin:
            print("input>")
            # Lit une ligne si disponible (non-bloquant)
            line = sys.stdin.readline()
            if line:
                line = line.strip()
                print("REPL:", line)
                if line == "start":
                    message = "start\n".encode()
                    n = len(message)
                    if uart.write(message) == n:
                        print("envoi de start")

        else:
            print("no input")
    except:
        pass


