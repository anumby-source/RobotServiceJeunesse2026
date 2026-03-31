# Procédure d'installation des Robots pour RSJ2026

Les addresses MAC des CPU robots et télécommandes sont à jour dans `Python/mac_addr.py`

Il faut mettre à jour l'addresse MAC du CPU-base dans `Python/mac_addr.py` avant de charger dans les différents CPU

Les programmes `robot.py` ET `telecommande.py` savent détecter automatiquement le numéro de Robot qui leur correspond

## Tous les fichers à installer dans les différents CPUs pour SJ2026:

K210:
- CCW/main.py
- CCW/model-259097.kmodel

CPU Robot:
- Python/boot.py
- Python/dcMotor.py
- Python/mac_addr.py
- Python/main.py
- Python/robot.py

CPU télécommande:
- Python/boot.py
- Python/mac_addr.py
- Python/main.py
- Python/st7789_170x320.py
- Python/telecommande.py
- russhughes/*

CPU base:
- Python/base.py
- Python/server_async.py
- Python/simple_queue.py


