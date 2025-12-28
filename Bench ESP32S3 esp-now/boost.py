import network

MAC = network.WLAN().config("mac")
MACA= b'\xd0\xcf\x13C\xa7$'
MACB = b'\xd0\xcf\x13D\x0b\x1c'

print("MAC=", MAC)

print("MACA=", MACA)
print("MACB=", MACB)

print("MAC=", MAC, "MACA=", MACA, "MACB=", MACB)

moi = ""
if MAC == MACA:
    moi = "MACA"
else:
    moi = "MACB"

print("Je suis", moi)


