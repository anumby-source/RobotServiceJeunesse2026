import network

MAC = network.WLAN().config("mac")
MACA= b'\xd0\xcf\x13C\xa7$'
MACB = b'\xd0\xcf\x13D\x0b\x1c'
MACC = b'\xac\xa7\x04\xee\xe4\xb8'

print("MAC=", MAC)

print("MACA=", MACA)
print("MACB=", MACB)
print("MACC=", MACC)

print("MAC=", MAC, "MACA=", MACA, "MACB=", MACB, "MACC=", MACC)

moi = ""
if MAC == MACA:
    moi = "MACA"
elif MAC == MACB:
    moi = "MACB"
else:
    moi = "MACC"

print("Je suis", moi)


