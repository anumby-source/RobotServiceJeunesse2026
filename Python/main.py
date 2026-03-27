# put your code here
#
#  mac_addr =   # this device

from mac_addr import *

num, cpu = find_robot()

if cpu == "telecommande":
    import png
    import telecommande
elif cpu == "robot":
    import robot
else:
    import simulate_espnow
    

