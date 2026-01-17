# Mise en place d'une communication série entre K210 et un ESP32

Dans le but de mettre en place une meilleure ergonomie de l'apprentissage pour des figures avec le K210, on teste la communication série UART.

On prépare une petite configuration

- un ESP32-C3 Super Mini 
- un K210 UnitV
- une diode (avec une résistance) pour visualiser le trafic
- deux logiciels 
  - envoi de messages par le ESP32
  - réception par le K210

![img.png](img.png)

![setup.png](setup.png)

- on utilise la broche 5 (TX) du ESP32-C3
- une diode est installée pour visualiser le trafic
- on connecte la broche 5 du ESP32 à la broche 1 (RX) du connecteur Grove

# Exécution:

sender.py:

    821971436 sent message from ESP32 #1 21
    821971437 sent message from ESP32 #2 21
    821971438 sent message from ESP32 #3 21
    821971439 sent message from ESP32 #4 21
    821971440 sent message from ESP32 #5 21
    821971441 sent message from ESP32 #6 21
    821971442 sent message from ESP32 #7 21
    821971443 sent message from ESP32 #8 21

receiver.py

    line b'message from ESP32 #37message from ESP32 #38'
    line b'message from ESP32 #39'
    line None
    line None
    line None
    line None
    line None
    line None
    line None
    line b'message from ESP32 #40'
    line None
    line None
    line None
    line None
    line None
    line None
    line b'message from ESP32 #41'
    line None
    line None
    line None
    line None
    line None
    line None
    line None
    line b'message from ESP32 #42'
    line None
    line None
    line None
    line None
    line None
    line None
    line None
    line b'message from ESP32 #43'
    line None
    line None
    line None
    line None
    line None
