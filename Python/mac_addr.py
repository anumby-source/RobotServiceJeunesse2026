import network

robot_mac = {
    1 : b'H\xf6\xeez/\xd4',
    2 : b'H\xf6\xeez0(',
    3 : b'H\xf6\xeez0\x0e',
    4 : b'H\xf6\xeez/,',
    5 : b'H\xf6\xeez3\x84',
    6 : b'H\xf6\xeez4&',
    7 : b'',
    8 : b'H\xf6\xeez/\xf6'
    }

telecommande_mac = {
#     1 : b'x!\x84\x88\xae\xdc',
    1 : b'\x88\x13\xbf\xfc\xe3\xbc',
    2 : b'\x88\x13\xbf\xfc\xe8\xf0',
    3 : b'\x88\x13\xbf\xfc\xe4\xfc',
    4 : b'\x88\x13\xbf\xfc\xe9p',
    5 : b'\x88\x13\xbf\xfc\xce\xe0',
    6 : b'\x88\x13\xbf\xfc\xe5|',
    7 : b'',
    8 : b'\x88\x13\xbf\xfc\xe5\x80'
    }

print("Mon adresse MAC:", network.WLAN().config("mac"))

def find_robot():
    mac = network.WLAN().config("mac")
    for i in robot_mac:
        if mac == robot_mac[i]:
            print("je suis le robot n°", i)
            return i, "robot"
    print("no robot")
    for i in telecommande_mac:
        if mac == telecommande_mac[i]:
            print("je suis la telecommande n°", i)
            return i, "telecommande"
    print("no télécommande")
    return None, "unknown robot"
