# setup the camera
import sensor
import lcd
import time
from machine import UART
from fpioa_manager import fm

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_windowing((224, 224))

sensor.run(1)

lcd.init()

class_num = 3
sample_num = 15
class_names = ['stop', 'sens-interdit', 'dep-interdit']

# Setup UART
fm.register(34, fm.fpioa.UART2_RX, force=True)
uart = UART(UART.UART2, 115200, 8, None, 1, timeout=1000, read_buf_len=4096)


def draw_string(img, x, y, text, color, scale, bg=None):
    if bg:
        img.draw_rectangle(x - 2, y - 2, len(text) * 8 * scale + 4, 16 * scale, fill=True, color=bg)
    img = img.draw_string(x, y, text, color=color, scale=scale)
    return img


import gc

try:
    del model
except Exception:
    pass
try:
    del classifier
except Exception:
    pass
gc.collect()

# model = kpu.load(0x300000)
# classifier = kpu.classifier(model, class_num, sample_num) # ajouter  ", fea_len=512)" pour le modèle lite

t0 = time.ticks_ms()

c = 0
while True:
    img = sensor.snapshot()
    lcd.display(img)

    t = time.ticks_ms()
    dt = t - t0
    print("dt:", dt)
    if uart.any():
        line = uart.readline()
        print("line", line)
        try:
            c = int(line)
            # index = classifier.add_class_img(img)
            print("add class img:", c)
            if c >= (class_num - 1):
                break
        except:
            pass

    time.sleep_ms(20)






