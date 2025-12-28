# Tests esp-now entre deux ESP32S3

## Configuration: deux ESP32S3 
- **boost.py**
  - boost est commun aux deux ESP32S3. Il contient la configuration MAC des deux ESP32S3
- **ESPA**:
  - ESPA est configuré avec son main.py puis est alimenté par une powerbank
  - ESPA attend le message "START" puis envoie 10 messages "OK" à l'émetteur du START
- **ESPB**:
  - ESPB envoie "START" à ESPA puis reçoit des messages de la part de ESPA. On peut relancer à volonté ESPB.



      MAC= b'\xd0\xcf\x13D\x0b\x1c'
      MACA= b'\xd0\xcf\x13C\xa7$'
      MACB= b'\xd0\xcf\x13D\x0b\x1c'
      MAC= b'\xd0\xcf\x13D\x0b\x1c' MACA= b'\xd0\xcf\x13C\xa7$' MACB= b'\xd0\xcf\x13D\x0b\x1c'
      Je suis MACB
      WiFi prêt, MAC : b'\xd0\xcf\x13D\x0b\x1c'
      Envoi de START à ESP A...
      START envoyé !
      Réception des OK...
      Reçu : b'OK' de b'\xd0\xcf\x13C\xa7$'
      Reçu : b'OK' de b'\xd0\xcf\x13C\xa7$'
      Reçu : b'OK' de b'\xd0\xcf\x13C\xa7$'
      Reçu : b'OK' de b'\xd0\xcf\x13C\xa7$'
      Reçu : b'OK' de b'\xd0\xcf\x13C\xa7$'
      Reçu : b'OK' de b'\xd0\xcf\x13C\xa7$'
      Reçu : b'OK' de b'\xd0\xcf\x13C\xa7$'
      Reçu : b'OK' de b'\xd0\xcf\x13C\xa7$'
      Reçu : b'OK' de b'\xd0\xcf\x13C\xa7$'
      Reçu : b'OK' de b'\xd0\xcf\x13C\xa7$'



