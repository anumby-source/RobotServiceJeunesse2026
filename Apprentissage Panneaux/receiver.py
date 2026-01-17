from fpioa_manager import fm
from machine import UART
import time

# Setup UART
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

# on crée le dictionnaire de toutes les images à acquérir
# cette liste est accumulée au fur et à mesure des captures.
# on associe chaque image à l'identifiant fourni à chaque message.

images = dict()

# on ignore le premier message qui pourrait contenir un identifiant mas formé
started = False

# Loop
while True:
    img = sensor.snapshot()
    lcd.display(img)
    if uart.any():
        line = uart.readline()
        if not started:
            started = True
            continue
        print("line", line)
        try:
            n = int(line.strip())
            print("identifiant {:02d}".format(n))
            if n in images:
                image_num = images[n]
                image_num += 1
                images[n] = image_num
                # index = classifier.add_sample_img(img)
                # print("add sample img:", index)
            else:
                images[n] = 1
                # index = classifier.add_class_img(img)
                # print("add class img:", index)

            # ici on va capturer cette image, et l'enregistrer dans le modèle
            # et on va l'associer à cet identifiant.
        except:
            # ici on va analyser une commande particulière
            # - fin des capturez et training

            pass
        print("-----------", sorted(images.items()))
    time.sleep_ms(30)

