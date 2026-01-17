 Apprentissage panneaux routiers
 
- sender.py:
    - on saisit les identifiants. Chaque identifiant envoyé va déclencher la capture de l'image actuellement cadrée.
    - on stop la série de captures par le mot "stop"
- receiver.py:
    - chaque image capturée est associée à son idenfiant et stockée dans un dictionnaire
    - puis lorsque l'on reçoit "stop", alors on va installer toutes les images (ordonnées) dans fichier classifier
    - et ensuite on active le training et la sauvegarde du nouveau modèle.
  

Sender:

        id [1..12] () 3
        id [1..12] (3) 
        id [1..12] (3) 
        id [1..12] (3) 2
        id [1..12] (2) 
        id [1..12] (2) 5
        id [1..12] (5) 
        id [1..12] (5) 6
        id [1..12] (6) 
        id [1..12] (6) 7
        id [1..12] (7) 
        id [1..12] (7) 
        id [1..12] (7) stop
        id [1..12] (7) 

Receiver:

        line b'02'
        identifiant 02
        set image to class  2 [(2, 1)]
        line b'02'
        identifiant 02
        set image to class  2 [(2, 2)]
        line b'02'
        identifiant 02
        set image to class  2 [(2, 3)]
        line b'05'
        identifiant 05
        set image to class  5 [(2, 3), (5, 1)]
        line b'05'
        identifiant 05
        set image to class  5 [(2, 3), (5, 2)]
        line b'05'
        identifiant 05
        set image to class  5 [(2, 3), (5, 3)]
        line b'05'
        identifiant 05
        set image to class  5 [(2, 3), (5, 4)]
        line b'05'
        identifiant 05
        set image to class  5 [(2, 3), (5, 5)]
        line b'05'
        identifiant 05
        set image to class  5 [(2, 3), (5, 6)]
        line b'05'
        identifiant 05
        set image to class  5 [(2, 3), (5, 7)]
        line b'05'
        identifiant 05
        set image to class  5 [(2, 3), (5, 8)]
        line b'07'
        identifiant 07
        set image to class  7 [(2, 3), (5, 8), (7, 1)]
        line b'stop'
        ----------- 5 8 [{"w":224, "h":224, "type"="rgb565", "size":100352}, {"w":224, "h":224, "type"="rgb565", "size":100352}, {"w":224, "h":224, "type"="rgb565", "size":100352}, {"w":224, "h":224, "type"="rgb565", "size":100352}, {"w":224, "h":224, "type"="rgb565", "size":100352}, {"w":224, "h":224, "type"="rgb565", "size":100352}, {"w":224, "h":224, "type"="rgb565", "size":100352}, {"w":224, "h":224, "type"="rgb565", "size":100352}]
        ----------- 2 3 [{"w":224, "h":224, "type"="rgb565", "size":100352}, {"w":224, "h":224, "type"="rgb565", "size":100352}, {"w":224, "h":224, "type"="rgb565", "size":100352}]
        ----------- 7 1 [{"w":224, "h":224, "type"="rgb565", "size":100352}]
        MicroPython v0.5.0-98-g7ec09ea22-dirty on 2020-07-21; Sipeed_M1 with kendryte-k210
        Type "help()" for more information.
        >>> 