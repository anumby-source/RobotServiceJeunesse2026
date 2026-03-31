#           rotation=0                     rotation=1
#           ----------                      ----------
#          |   TTGO   |                    |   TTGO   |
#           ----------                      ----------
#     (0,0)|    x     |(134,0)      (0,134)|    y     |(0,0)
#          |    ->    |                    |    <-    |
#          |          |                    |          |
#          | y |      |                    | x |      |
#          |   v      |                    |   v      |
#          |          |                    |          |
#   (0,239)|          |(134,239)  (239,134)|          |(239,0)
#           ----------                      ----------
#
#
#           rotation=2                     rotation=3
#           ----------                      ----------
#          |   TTGO   |                    |   TTGO   |
#           ----------                      ----------
# (134,239)|    x     |(0,239)      (239,0)|    y     |(239,134)
#          |    <-    |                    |    ->    |
#          |          |                    |          |
#          | y ^      |                    | x ^      |
#          |   |      |                    |   |      |
#          |          |                    |          |
#   (134,0)|          |(0,0)          (0,0)|          |(0,134)
#           ----------                      ----------
#
from machine import Pin, SPI
import st7789

# pour les arguments de st7789.ST7789, voir https://github.com/russhughes/st7789_mpy

tft = st7789.ST7789(SPI(2, baudrate=40_000_000, sck=Pin(18), mosi=Pin(19), miso=None)
                      , 135, 240                   # width, height
                      , reset=Pin(23, Pin.OUT)     # chip hard reset
                      , cs=Pin(5, Pin.OUT)         # chip select pin
                      , dc=Pin(16, Pin.OUT)        # data/command pin
                      , backlight=Pin(4, Pin.OUT)  # backlignt pin (often left floating)
                      , rotation=0                 # 0=portrait, 1=landscape(90°), 2=reverse prtrait(180°), 3=reverse landscape(270°)
                      , options=0                  # 0=no wrap, 1=wrap vertically, 2=wrap horizontally, 3=wrap both
                      , buffer_size=0
                      )

tft.init()
