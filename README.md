Projet RobotServiceJeunesse2026



# Réflexions préparatoires pour le projet Jeunesse 2026

Le projet Jeunesse aura lieu dans une 1/2 journée dans les vacances pâques 2026 à choisir. 
Faire attention pour la durée: discuter avec les organisateurs pour obtenir réellement les 3 heures de le demie journée.

Principe: On garde le proto de l'année dernière mais avec quelques corrections (et/ou améliorations)

- Meilleurs moteurs plus rapides (choix des roues)
- Mener des tests pour fiabiliser l'utilisation de Esp now
- choisir le CPU de base: Esp32 s2 s3? C3?
  - impact: nombre de DIOs
  - tester la nécessité d'une vraie antenne
  - Nouveau proto (encombrement)
- Pilotage
- nouveau design pour le circuit
- utilisation d'un Microphone?
- IA ? Reconnaissance de symboles plutôt que caractères

- Refaire la télécommande. tests de Fiabilité
- Pb de multicanal sur la communication: tests
- utilisation de Powerbank 5V
- Reconnaissance par le k210 ?

## Organisation:
- distribuer les rôles pour les éléments à re-tester (moteurs, communication, reconnaissance, circuit, achats)
- mettre en place un Github 2026

# Benchmark ESP-now sur ESP32 S3

En menant mon benchmark esp-now j'ai compris qu'il faut flasher micropython >= 1.26 (au moins) car c'est à partir de cette version de micropython que Esp-now, est inclus dans micropython.
Par défaut 1.19 était flashé sur le ESP32-S3.
Pas grave mais il suffisait de le savoir.
