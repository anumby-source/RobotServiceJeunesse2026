import network

robot_mac = {
    1 : b'H\xf6\xeez/\xd4',
    2 : b'H\xf6\xeez0(',
    3 : b'',
    4 : b'',
    5 : b'',
    6 : b'',
    7 : b''
    }

telecommande_mac = {
#     1 : b'x!\x84\x88\xae\xdc',
    1 : b'\x88\x13\xbf\xfc\xe3\xbc',
    2 : b'\x88\x13\xbf\xfc\xe8\xf0',
    3 : b'',
    4 : b'',
    5 : b'',
    6 : b'',
    7 : b''
    }

baseAddr = b'$X|\x91\xe0\xd8'
baseAddr = b'\xd0\xcf\x13C\xa7$'
baseAddr = b'\xac\xa7\x04\xee\xe4\xb8'

print("Mon adresse MAC:", network.WLAN().config("mac"))

def find_robot():
    mac = network.WLAN().config("mac")
    for i in robot_mac:
        if mac == robot_mac[i]:
            return i, "robot"
    for i in telecommande_mac:
        if mac == telecommande_mac[i]:
            return i, "telecommande"
    return None
