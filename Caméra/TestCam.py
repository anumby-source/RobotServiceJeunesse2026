# setup the camera
import sensor
import lcd

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_windowing((224, 224))

# applique un miroir sans changer droite-gauche
# sensor.set_hmirror(sensor_hmirror)

# inverse droite-gauche
# sensor.set_vflip(sensor_vflip)

sensor.run(1)

lcd.init()

while True:
    img = sensor.snapshot()
    lcd.display(img)
    # time.sleep(1)


