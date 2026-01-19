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

# on crÃ©e le dictionnaire de toutes les images Ã  acquÃ©rir
# cette liste est accumulÃ©e au fur et Ã  mesure des captures.
# on associe chaque image Ã  l'identifiant fourni Ã  chaque message.

images = dict()

def show(images):
    s = dict()
    for k in images:
        l = images[k]
        s[k] = len(l)
    return sorted(s.items())


# on ignore le premier message qui pourrait contenir un identifiant mas formÃ©
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
                image_list = images[n]
                image_list.append(img)
                images[n] = image_list
                print("set image to class ", n, show(images))
            else:
                images[n] = [img]
                print("set image to class ", n, show(images))

        except:
            if line == b"stop":
                break
            continue

    time.sleep_ms(30)

#analyse des images capturÃ©es

for k in images:
    image_list = images[k]
    print("-----------", k, len(image_list), image_list)


    # index = classifier.add_sample_img(img)
    # print("add sample img:", index)
    # index = classifier.add_class_img(img)
    # print("add class img:", index)
    # ici on va capturer cette image, et l'enregistrer dans le modÃ¨le
    # et on va l'associer Ã  cet identifiant.

# - fin des capturez et training
