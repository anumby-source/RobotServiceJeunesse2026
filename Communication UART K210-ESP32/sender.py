from machine import UART
import time

# setup UART
uart = UART(1, baudrate=9600, tx=5, rx=6)

# loop
i = 0
while True:
    i += 1
    message = 'message from ESP32 #' + f"{i}"
    n = uart.write(message)
    print(time.time(),"sent", message, n)
    time.sleep(1)
