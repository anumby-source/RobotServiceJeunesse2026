# Développements Python

## Librairies

- `camera_init.py`: contient la fonction `camera_init()` pour initialiser la caméra OV2640
- `server.py`: contient la classe `Server` pour définir un serveur Web en mode AP_IF avec une IHM minimale

## Programmes

- `InitDataset.py`: Création d'un dataset en capturant N copies d'images de panneaux routiers imprimées avec une caméra OV2640 en faisant varier l'exposition, le cadrage, la distance de prise de vue. On crée les images dans le dossier `dataset/images/photo_<classe>_<n>.jpg`
- `detourage.py`: Création des fichiers d'annotation XML au format Pascal VOC à partir d'un ensemble d'images. On crée les Bounding Box soit automatiquement, soit par modification manuelle. Les annotations sont créées dans le dossier `dataset/xml/photo_<classe>_<n>.xml`
- `control.py`: émulation du scénario de jeu
- `redimensionner`: redimensionner les panneaux
