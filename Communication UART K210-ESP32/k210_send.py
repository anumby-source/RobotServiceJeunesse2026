from fpioa_manager import fm
from machine import UART
import time


# Setup UART in receiver
fm.register(34, fm.fpioa.UART2_RX, force=True)
fm.register(35, fm.fpioa.UART2_TX, force=True)
uart = UART(UART.UART2, 115200, 8, None, 1, timeout=1000, read_buf_len=4096)

# setup the camera
import sensor
import lcd

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_windowing((224, 224))
lcd.init()

# Loop
i = 0
while True:
    img = sensor.snapshot()
    lcd.display(img)
    msg = "from UnitV " + str(i)
    print("send " + msg)
    uart.write(msg + "\n")
    i += 1
    time.sleep_ms(3000)



