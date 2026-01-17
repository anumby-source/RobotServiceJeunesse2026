from fpioa_manager import fm
from machine import UART
import time


# Setup UART in receiver
fm.register(34, fm.fpioa.UART2_RX, force=True)
uart = UART(UART.UART2, 9600, 8, None, 1, timeout=1000, read_buf_len=4096)

# setup the camera
import sensor
import lcd

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_windowing((224, 224))
lcd.init()

# Loop
while True:
    img = sensor.snapshot()
    lcd.display(img)
    print("line", uart.readline())
    time.sleep_ms(30)

