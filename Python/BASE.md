# Programme de base pour le jeu Robot

![img_1.png](img_1.png)

Le programme base.py implémente la connexion entre le cpu du Robot et l'écran de contrôle

Le principe de base consiste à recevoir les messages (canal espnow) qui reflètent les panneaux routiers détectés par la caméra du K210.

![img_2.png](img_2.png)

l'IHM de base.py montre tous les messages reçus et décode ces messages en allumant les boutons des panneaux.

Etat d'avancement du programme de base:

- le programme base tourne sur un esp32
- c'est un serveur Web utilisant les SSE
- il est connecté espnow avec le CPU du robot.
  => il faudra assurer que la mac adresse du ESP32 de base est déclarée
     dans le fichier mac_addr 
- actuellement la base est sensible aux valeurs d'ID de panneaux transférés via espnow mais il est 
  aussi sensible de façon équivalente aux boutons équivalents de l'IHM de la base
- il reste à ajouter la propagation des valeur de la vitesse (0, v1, v2) qui est nécessaire pour
  faire fonctionner le protocole du jeu.
- actuellement du protocole de jeu est simplifié
   - on attend la reconnaissance du panneau "start"
   - ensuite tous les panneaux sont reconnus mais n'influence pas le jeu
   - en suite la reconnaissance de "stop" arrête le jeu
   - l'IHM met à jour le temps courant de parours
   - on ne comptabilise pas le pénalités pour l'instant

