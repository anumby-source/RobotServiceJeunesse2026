 Apprentissage panneaux routiers
 
- sender.py:
    - on saisit les identifiants. Chaque identifiant envoyé va déclencher la capture de l'image actuellement cadrée.
    - on stop la série de captures par le mot "stop"
  - receiver.py:
    - chaque image capturée est associée à son idenfiant et stockée dans un dictionnaire
    - puis lorsque l'on reçoit "stop", alors on va installer toutes les images (ordonnées) dans fichier classifier
    - et ensuite on active le training et la sauvegarde du nouveau modèle.
  