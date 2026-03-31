"""
jpg.py

    Draw a full screen jpg using the slower but less memory intensive method of blitting
    each Minimum Coded Unit (MCU) block. Usually 8×8pixels but can be other multiples of 8.

    bigbuckbunny.jpg (c) copyright 2008, Blender Foundation / www.bigbuckbunny.org
"""

import random
import st7789
import tft_config
import time

tft = tft_config.config(3)

def main():
    '''
    Decode and draw jpg on display
    '''

    tft.init()
    while True:
        try:
            print(f'bigbuckbunny-{tft.width()}x{tft.height()}.jpg')
            tft.jpg(f'bigbuckbunny-{tft.width()}x{tft.height()}.jpg', 0, 0, st7789.SLOW)
            time.sleep(2)
            tft.jpg(f'nasa01.jpg', 0, 0, st7789.SLOW)
            time.sleep(2)
            tft.jpg(f'nasa14.jpg', 0, 0, st7789.SLOW)
            time.sleep(2)
        except KeyboardInterrupt:
            break

os.chdir('/russhughes/demos')
main()
