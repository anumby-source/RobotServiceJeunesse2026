from fpioa_manager import fm
from machine import UART
import time
import os
import uos

images = 0

# Setup UART
fm.register(34, fm.fpioa.UART2_RX, force=True)
fm.register(35, fm.fpioa.UART2_TX, force=True)
uart = UART(UART.UART2, 115200, 8, None, 1, timeout=1000, read_buf_len=4096)

def clear_uart_buffer(uart):
    while uart.any():
        uart.read()  # Lit et jette les données restantes
    time.sleep_ms(10)

clear_uart_buffer(uart)

# setup the camera
import sensor
import lcd

sensor.reset()
pixel_format = sensor.RGB565  # ou sensor.GRAYSCALE
sensor.set_pixformat(pixel_format)
sensor.set_framesize(sensor.QVGA)
sensor.set_windowing((224, 224))
lcd.init()

def send_image_over_uart(img):
    width = img.width()
    height = img.height()
    bytes_per_pixel = 2  # RGB565
    size_bytes = width * height * bytes_per_pixel
    img_data = img.to_bytes()

    # Taille des paquets (en bytes)
    PACKET_SIZE = 128*8*8*2
    num_packets = (size_bytes + PACKET_SIZE - 1) // PACKET_SIZE

    # Envoi de l'en-tête (résolution, taille totale, nombre de paquets)

    # header = "<IMG:{width},{height},{size_bytes},{num_packets}>"
    header = "<IMG:{:05d},{:05d},{:05d},{:05d},{:05d},{:05d}>".format(images, PACKET_SIZE, width, height, size_bytes, num_packets)

    print("header", header)
    uart.write(header)
    time.sleep_ms(10)

    # Envoi des paquets
    start = 0
    for i in range(num_packets):
        end = start + min(PACKET_SIZE, size_bytes - start)
        to_sent = end - start
        print("send  [", start, ",", end+1, "]", to_sent)
        packet = img_data[start:end+1]
        uart.write(packet)
        start = end
        time.sleep_ms(10)  # Petit délai pour éviter de saturer le buffer

    # print(f"Image envoyée : {width}x{height}, {size_bytes} bytes")
    print("Image envoyée : {}x{}, {} bytes".format(width, height, size_bytes))


import KPU as kpu

while True:
    while True:
        # print("waiting for start")
        if uart.any():
            line = uart.readline().strip()
            print("line=", line)
            if line == b"start":
                started = True
                print("started", line)
                clear_uart_buffer(uart)
                break
        time.sleep(1)

    num = 2
    for i in range(num):
        img = sensor.snapshot()
        lcd.display(img)
        path = "image{:02d}.jpg".format(i)
        print("\n>>>send image #", path)
        send_image_over_uart(img)
        images += 1
        time.sleep_ms(10)

