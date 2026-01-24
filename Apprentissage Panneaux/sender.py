from machine import UART
import time
import random

uart = UART(1, baudrate=115200, tx=5, rx=6)

# on suppose le nombre d'images
images = 3
samples = 5

while True:
    message = "classes={:02d}\n".format(images).encode()
    n = len(message)
    if uart.write(message) == n:
        print("envoi du numbre de classes=", images)
        break

while True:
    message = "samples={:02d}\n".format(samples).encode()
    n = len(message)
    if uart.write(message) == n:
        print("envoi du numbre de samples=", samples)
        break


# on crée un message qui contient l'identifiant de l'image à capturer
def build_msg(N):
    if not (0 <= N <= images - 1):
        raise ValueError(f"N doit être entre 0 et {images - 1}")
    return "{:02d}".format(N).encode()


i = 0
while True:
    message = b'message from ESP32 #' + f"{i}"
    command_text = input(f"id [0..{images - 1}] ({i}) ")
    if command_text == "":
        command_text = f"{i}"

    try:
        text = command_text.strip()
        if text == "stop":
            message = b"stop"
        else:
            r = int(text)
            if r >= 0 and r < images:
                message = build_msg(r)
                print("message=", message)
                i += 1
            else:
                continue
    except:
        continue

    n = uart.write(message)

    print(time.time(), "sent", message)

    if i >= images:
        break

print("classes initialized")
