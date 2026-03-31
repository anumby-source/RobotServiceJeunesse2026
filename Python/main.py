# put your code here
#
#  mac_addr =   # this device

from mac_addr import *

num, cpu = find_robot()
if cpu == "telecommande":
    print("telecommande", num)
    import png
    import telecommande
elif cpu == "robot":
    print("Robot", num)
    import robot
else:
    print("esp_receive")
    import esp_receive
    

