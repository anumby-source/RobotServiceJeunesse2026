import network
import espnow
from machine import Pin, ADC
from time import sleep_ms, ticks_ms
# from neopixel import NeoPixel
from mac_addr import robot_mac, telecommande_mac

#
num = 1
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
    try:
        r, s = a0.read_uv()/1000, a1.read_uv()/1000
        r = normalize(r, ramp)     # r in [-ramp,+ramp]
        s = normalize(s, samp)     # s in [-samp,+samp]
        ls, rs = constrain(s+r), constrain(s-r)
        cmd = 'ml.set_speed(' + str(ls) + ')\r'
        cmd += 'mr.set_speed(' + str(rs) + ')\r'
        e.send(robotAddr, cmd.encode(), False)
        print(cmd.encode())
        sleep_ms(100)
    except:
#         np[0] = red
#         np.write()
        break 