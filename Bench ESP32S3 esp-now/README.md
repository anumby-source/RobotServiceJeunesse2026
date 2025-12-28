# Tests esp-now entre deux ESP32S3

## Configuration: deux ESP32S3 
- **boost.py**
  - boost est commun aux deux ESP32S3. Il contient la configuration MAC des deux ESP32S3
- **ESPA**:
  - ESPA est configuré avec son main.py puis est alimenté par une powerbank
  - ESPA attend le message "START" puis envoie 10 messages "OK" à l'émetteur du START
- **ESPB**:
  - ESPB envoie "START" à ESPA puis reçoit des messages de la part de ESPA. On relance la boucle.



    MAC= b'\xd0\xcf\x13D\x0b\x1c'
    MACA= b'\xd0\xcf\x13C\xa7$'
    MACB= b'\xd0\xcf\x13D\x0b\x1c'
    MAC= b'\xd0\xcf\x13D\x0b\x1c' MACA= b'\xd0\xcf\x13C\xa7$' MACB= b'\xd0\xcf\x13D\x0b\x1c'
    Je suis MACB
    WiFi prêt, MAC : b'\xd0\xcf\x13D\x0b\x1c'
    Envoi de START à ESP A...
    START envoyé !
    Réception des OK...
    OK reçu: 1 / 10
    OK reçu: 2 / 10
    OK reçu: 3 / 10
    OK reçu: 4 / 10
    OK reçu: 5 / 10
    OK reçu: 6 / 10
    OK reçu: 7 / 10
    OK reçu: 8 / 10
    OK reçu: 9 / 10
    OK reçu: 10 / 10
    Timeout ou message inconnu
    Réception terminée !
    Envoi de START à ESP A...
    START envoyé !
    Réception des OK...
    OK reçu: 1 / 10
    OK reçu: 2 / 10
    OK reçu: 3 / 10
    OK reçu: 4 / 10
    OK reçu: 5 / 10
    OK reçu: 6 / 10
    OK reçu: 7 / 10
    OK reçu: 8 / 10
    OK reçu: 9 / 10
    OK reçu: 10 / 10
    Timeout ou message inconnu
    Réception terminée !



