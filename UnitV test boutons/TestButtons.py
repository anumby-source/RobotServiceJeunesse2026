from Maix import GPIO
from fpioa_manager import fm

# utilisation des bouton A et B du module UnitV

A = 18
B = 19
fm.register(A, fm.fpioa.GPIO0)
keyA = GPIO(GPIO.GPIO0, GPIO.IN, GPIO.PULL_UP)
fm.register(B, fm.fpioa.GPIO2)
keyB = GPIO(GPIO.GPIO2, GPIO.IN, GPIO.PULL_UP)

while True:
    print("A=", keyA.value(), "B=", keyB.value())
