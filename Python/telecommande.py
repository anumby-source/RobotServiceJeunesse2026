import network
import espnow
from machine import Pin, ADC
from time import sleep_ms, ticks_ms
# from neopixel import NeoPixel
from mac_addr import *

import st7789 
import tft_config
import vga2_bold_16x32 as font16x32
import vga1_8x8 as font8x8

tft = tft_config.config(1)

tft.init()
tft.fill(st7789.BLACK)

ZONE_Y = 40
ZONE_H = 50

last_text = None

def center(text, font=font8x8):
    global last_text
    
    # Dimensions écran
    W = tft.width()
    H = tft.height()

    # Taille police
    char_w = font.WIDTH
    char_h = font.HEIGHT
    
    # Largeur du texte
    length = 1 if isinstance(text, int) else len(text)
    text_w = length * char_w
    

    # Position centrée
    x = (W - text_w) // 2
    y = ZONE_Y + (ZONE_H - char_h) // 2
    
    if last_text is not None:
        old_w = len(last_text) * char_w
        old_x = (W - old_w) // 2
        old_y = y
        tft.fill_rect(old_x, old_y, old_w, char_h, st7789.BLACK)
    
    tft.rect(10, ZONE_Y, 220, ZONE_H, st7789.WHITE)
    tft.text(
        font,
        text,
        x,
        y,
        st7789.WHITE,
        st7789.BLACK)
    
    last_text = text

#
num, _ = find_robot()
robotAddr = robot_mac[num]

#
# red, green, blue, white, black = (0, 128, 0), (128, 0, 0), (0, 0, 128), (32, 32, 32), (0, 0, 0)

#
def normalize(x, amp=100):
    ''' resize x -> [-amp;+amp] '''
    x -= midadc
    if x > dzw:
        x = int(amp*(x-dzw)/szw)
    elif x < -dzw:
        x = int(amp*(x+dzw)/szw)
    else:
        x = 0
    return x
#
def constrain(x):
    return min(max(x, -100), 100)

# init ADC
a0 = ADC(Pin(39, Pin.IN), atten=ADC.ATTN_11DB)
a1 = ADC(Pin(36, Pin.IN), atten=ADC.ATTN_11DB)
midadc = 1730         # adc middle
maxadc = 3150         # adc max
dzw    = 200          # dead zone width
szw    = midadc - dzw # sensitive zone width
samp   = 100
ramp   = 50

# init neopixel
# np = NeoPixel(Pin(5, Pin.OUT),1)
# np[0] = (8, 8, 8)
# np.write()

# A WLAN interface must be active to send()/recv()
sta = network.WLAN(network.STA_IF)  # Or network.AP_IF
sta.active(True)
sta.disconnect()      # For ESP8266

# init espnow
e = espnow.ESPNow()
e.active(True)
print("telecommande.py : Network active, Espnow ok")

try:
    e.add_peer(robotAddr)      # Must add_peer() before send()
except:
    pass
print("telecommande.py : robot added to peers")
#
while True:
    r, s = a0.read_uv()/1000, a1.read_uv()/1000
    r = normalize(r, ramp)     # r in [-ramp,+ramp]
    s = normalize(s, samp)     # s in [-samp,+samp]
    ls, rs = constrain(s+r), constrain(s-r)
    cmd = 'ml.set_speed(' + str(ls) + ')\r'
    cmd += 'mr.set_speed(' + str(rs) + ')\r'
    e.send(robotAddr, cmd.encode(), False)
    # print(cmd.encode())
    center(f"ls={ls} rs={rs}", font=font16x32)
    sleep_ms(100)
    
