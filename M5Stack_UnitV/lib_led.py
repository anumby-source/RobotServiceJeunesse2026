from modules import ws2812

class Led:
    def __init__(self):
        self.led = ws2812(8,100)

        r, j, v, b, vi, blk = ((250, 0, 0),
                               (200, 32, 0),
                               (0, 128, 0),
                               (0, 0, 250),
                               (128, 0, 128),
                               (0, 0, 0))
        self.leds = (r, j, v, b, vi)

        self.set_led(blk)
        self.led.display()

    def set_let(self, ind):
        self.led.set_led(0, self.leds[ind])
        self.led.display()

    def reset_let(self):
        self.set_led(0, (0, 0, 0))
        self.led.display()

