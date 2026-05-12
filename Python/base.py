import uasyncio as asyncio
import urandom
from server_async import ServerAsync
from simple_queue import SimpleQueue
import time

from mac_addr import *
import espnow

# Initialisation Wi-Fi en mode station
sta = network.WLAN(network.STA_IF)
sta.active(True)

mac_base = sta.config('mac')
print("MAC de base :", mac_base)


# Initialisation d’ESP-NOW
e = espnow.ESPNow()
e.active(True)

esp_task = None

# définition des deux queues d'attente pour les événements
queue_sse = SimpleQueue()
queue_espnow = []

# gestion du jeu
class Jeu:
    def __init__ (self):
        self.reset()
    
    def reset(self):
        self.t0 = 0
        self.time = 0
        self.penalties = []
        self.running = False
        self.active = False
    
    def restart(self):
        self.active = True

    def start(self):
        if self.active:
            if not self.running:
                self.t0 = time.time()
                self.running = True
    
    def stop(self):
        if self.running:
            self.running = False
            self.active = False
    
    def now(self):
        return int(time.time() - self.t0)

# on va gérer deux joueurs (donc pour deux robots)
jeuA = Jeu()
jeuB = Jeu()

games = dict()
games['A'] = jeuA
games['B'] = jeuB
ids = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

# le dictionnaire contient les MAC adresses ordonnées par les ids
robots = dict()

simulation = True

def simul_robots():
    global robots
    
    robots = dict()
    # simulation sans aucun robot on simule la situation où les robots 3 et 5 se sont déclarés
    # cette situation existe quand on n'a pas de connection avec aucun robot.
    r1 = urandom.randint(0, 6)
    r2 = None
    while True:
        r2 = urandom.randint(0, 6)
        if r2 == r1: continue
        break
    robots[ids[len(robots)]] = robot_mac[r1]
    robots[ids[len(robots)]] = robot_mac[r2]
    print("simul_robots> Connect", r1, r2)

"""
IHM
"""

style=(
".g{margin-top:10px;display:flex;flex-direction:column;align-items:center;}"
".g table {margin:auto;}"
".g button{padding:10px;font-size:15px;background:green;color:#fff;border:none;border-radius:8px;}"
".log{margin-top:10px;max-height:150px;overflow:auto;font-family:monospace;}"
".status{font-size:15px;background:#ECECB9;color: black;display:inline-block;}"
".value{padding:5px;font-size:20px;color:red;max-height:20px;max-width:50px;resize:none;overflow:hidden;"
"}"
)


def body_side(side):
    return (
        
"<h2><button id='Robot" + side + "' onclick=fetch('/Robot" + side + "');>" + side + "</button></h2>"
"<div class='g'>"
"<table><tr>"
"<td>"
"<button id='" + side + "b7' onclick=" + side + "p(7);>Start</button>"
"</td>"
                        "</tr>"
                        "<tr>"
                                "<td>"
                                        "<button id='" + side + "b1' onclick=" + side + "p(1);>Limite 30</button>"
                                        "<button id='" + side + "b2' onclick=" + side + "p(2);>Cedez le passage</button>"
                                        "<button id='" + side + "b3' onclick=" + side + "p(3);>Passage pietons</button><br>"
                                        "<button id='" + side + "b4' onclick=" + side + "p(4);>Priorite a droite</button>"
                                        "<button id='" + side + "b5' onclick=" + side + "p(5);>Stationnement</button>"
                                "</td>"
                        "</tr>"
                        "<tr>"
                                "<td>"
                                        "<button id='" + side + "b6' onclick=" + side + "p(6);>Stop</button>"
                                "</td>"
                        "</tr>"
                "</table>"
        "</div>"
        "<div id='" + side + "status' class='status'>"
                "<p>Jeu</p>"
                "<table>"
                        "<tr>"
                                "<td>temps ecoule:</td><td><textarea id='" + side + "t1' class='value'>t1</textarea></td>"
                                "<td>penalites:</td><td><textarea id='" + side + "t2' class='value'>t2</textarea></td>"
                                "<td>temps total:</td><td><textarea id='" + side + "t3' class='value'>t3</textarea></td>"
                        "</tr>"
                "</table>"
        "</div>"
        "<div id='" + side + "log' class='log'>"
            "<p>xxx</p>"
        "</div>"
        )

def script_header_side(side):
    return (
        "var " + side + "L = document.getElementById('" + side + "log');"
        "function " + side + "p(i){fetch('/" + side + "btn/'+i);}"
        "window." + side + "p = " + side + "p;"
        "function " + side + "RB(){for(let i=1;i<=7;i++) document.getElementById('" + side + "b'+i).style.background='green';}"
        "window." + side + "RB = " + side + "RB;"
        )

"""
        "function RobotSelect" + side + "(n){document.getElementById('Robot" + side + "').value = n;}"
        "window.RobotSelect" + side + " = RobotSelect" + side + ";"
"""

def script_side(side):
    return (
            "if (key === '" + side + "PID') {"
              "var n = obj.split(',')[0];"
              "console.log('>>> key=' + key + ' obj=' + obj + ' n=' + n);"
              "" + side + "p(n);"
            "}"
            "if (key === '" + side + "BTN') {"
              "var n = obj.split(',')[0];"
              "console.log('>>> key=' + key + ' obj=' + obj + ' n=' + n);"
              # "" + side + "RB();"
              "document.getElementById('" + side + "b'+n).style.background='red';"
              "" + side + "L.appendChild(ligne);"
            "}"
            "if (key === '" + side + "VALUES') {"
                "const parts = obj.split(',');"
                "document.getElementById('" + side + "t1').value = parts[0] || '';"
                "document.getElementById('" + side + "t2').value = parts[1] || '';"
                "document.getElementById('" + side + "t3').value = parts[2] || '';"
                "" + side + "L.appendChild(ligne);"
            "}"
            "console.log('>>> key=' + key + ' obj=' + obj);"
            "if (key.startsWith('RobotSelect" + side + "')) {"
                "var num = key.split('(')[1];"
                "num = num.split(')')[0];"
                "obj = document.getElementById('Robot" + side + "');"
                "console.log('>>> obj='+ obj + ' Robot" + side + ".textContent= ' + num);"
                "obj.textContent = num || '';"
            "}"
        )

body=(
    "<button id='startBtn' onclick=fetch('/start') style=background:pink;>START</button>"
    "<button id='resetBtn' onclick=fetch('/reset');>RESET</button>"
    "<table><tr><td>"
    "" + body_side('A') + ""
    "</td><td>"
    "" + body_side('B') + ""
    "</td></tr></table>"
)

script=(
        "var E = new EventSource('/events');"
        "" + script_header_side('A') + ""
        "" + script_header_side('B') + ""
        "E.onmessage = function(e) {"
            "var m = e.data;"
            "key = m.split('=')[0];"
            "obj = m.split('=')[1];"
            "console.log('onmessage=' + m + ' key=' + key + ' obj=' + obj);"
            "var ligne = document.createElement('p');"
            "ligne.textContent = m;"
            "if (key === 'START') {"
              "AL.appendChild(ligne);"
              "BL.appendChild(ligne);"
              "document.getElementById('startBtn').style.background='red';"
            "}"
            "if (key === 'RESET') {"
               "console.log('resetting...');"
               "ARB();"
               "BRB();"
              "document.getElementById('startBtn').style.background='pink';"
            "}"
            "" + script_side('A') + ""
            "" + script_side('B') + ""
        "};"
)


# gestion des routes HTTP

async def play(robot_id, n):
    print("play> n=", n, "robot_id=", robot_id)
    n = str(int(n))

    jeu = games[robot_id]
    
    print("play> ")
    
    if n == '7':
        print("start")
        jeu.start ()


    if jeu.running:
        t = jeu.now()
        p = len(jeu.penalties)
        total = t + p
        values = robot_id + f"VALUES={t},{p},{total}"
        print("values=", values)
        await queue_sse.put(values)
        m = robot_id + "BTN=" + n
        print("m=", m)
        await queue_sse.put(robot_id + "BTN=" + n)
        
    if n == '6':
        print("stop")
        jeu.stop()
        

def find_robot_from_list(mac):
    for i in robot_mac:
        if mac == robot_mac[i]:
            return i
    return None
    
def robot_select(robot_id):
    side = robot_id[-1]
    try:
        num = find_robot_from_list(robots[side])
        print("robot_select> robot_id=", robot_id, robots, robot_id[-1], num)
        return num
    except:
        return None


async def http_handler(server, path, w):
    global esp_task
    global robots
    
    
    print("http_handler", path, jeuA.running, jeuB.running)
    if path.startswith("/Abtn/"):
        # simulation de la détection des panneaux du joueur A par clicks sur les boutons panneaux
        n = path.split("/")[-1]

        print("calling play> n=", n, "path[1]=", path[1])

        await play(path[1], n)
        await w.awrite("HTTP/1.1 200 OK\r\n\r\nOK")
        await w.aclose()        
        return True

    if path.startswith("/Bbtn/"):
        # simulation de la détection des panneaux du joueur B par clicks sur les boutons panneaux
        n = path.split("/")[-1]
        await play(path[1], n)
        await w.awrite("HTTP/1.1 200 OK\r\n\r\nOK")
        await w.aclose()
        return True
    
    if path.startswith("/RobotA"):
        print("RobotSelectA")
        num = robot_select(path)
        print(f"http_handler> RobotSelectA({num})")
        await queue_sse.put(f"RobotSelectA({num})")
        await w.awrite("HTTP/1.1 200 OK\r\n\r\nOK")
        await w.aclose()
        return True

    if path.startswith("/RobotB"):
        print("RobotSelectB")
        num = robot_select(path)
        print(f"http_handler> RobotSelectB({num})")
        await queue_sse.put(f"RobotSelectB({num})")
        await w.awrite("HTTP/1.1 200 OK\r\n\r\nOK")
        await w.aclose()
        return True

    if path.startswith("/start"):
        # gestion global du démarrage du jeu pour les deux joueurs
        await queue_sse.put("START")
        queue_espnow.clear()
        esp_task = asyncio.create_task(espnow_dispatcher())
        await w.awrite("HTTP/1.1 200 OK\r\n\r\nOK")
        await w.aclose()
        jeuA.restart()
        jeuB.restart()
        print("jeu START", jeuA.running, jeuB.running)
        return True

    if path=="/reset":
        # gestion global du reset du jeu pour les deux joueurs
        await queue_sse.put("RESET")
        if not esp_task is None:
            esp_task.cancel()
        jeuA.reset()
        jeuB.reset()
        values = f"AVALUES=0,0,0"
        print("values=", values)
        await queue_sse.put(values)
        values = f"BVALUES=0,0,0"
        print("values=", values)
        await queue_sse.put(values)
        await w.awrite("HTTP/1.1 200 OK\r\n\r\nOK")
        await w.aclose()
        print("jeuA RESET", jeuA.running)
        robots = dict()
        if simulation: simul_robots()
        return True

    return False


# gestion espnow
def get_robot_id(mac):
    global robots
    
    """
    le dict robots va enregistrer les adresses mac des robots qui envoient des messages espnow.
    à priori ceci ne concerne que 2 robots, mais sans que ce soit bloquant. Donc les valeurs
    du dict sont simplement le numéro d'arrivée des premiers messages des robots
    """

    if not mac in robots:
        robots[ids[len(robots)]] = mac
        
    id = ids[robots[mac]]

    return id

def on_recv(e):
    global robots
    global simulation
    
    # Attendre un message
    host, msg = e.recv()
    if msg:  # Un message est reçu
        print("Reçu de", host, ":", msg)
        # Si un robot envoie "HELLO"
        if msg == b"HELLO":
            if host not in robots:
                return
            print("Nouveau robot détecté :", host)

            if simulation:
                simulation = False
                robots = dict()
                
            id = ids[len(robots)]
            robots[id] = host

            # Ajouter robot comme peer
            try:
                e.add_peer(host)
            except OSError:
                pass  # déjà ajouté

            # Répondre avec l'adresse MAC de base
            payload = b"MASTER=" + mac_base
            e.send(host, payload)
            print("Réponse envoyée à", host)

            print("on_recv> ")
            num = find_robot_from_list(host)
            print(f"on_recv> RobotSelectA({num})")
            queue_espnow.append(f"RobotSelect{id}({num})")
        else:
            id = get_robot_id(host)
            print("on_recv> id=", id)
            txt = msg.decode('utf-8')
            # on convertit le format d'origine vers le format équivalent à l'appui d'un bouton
            txt = id + "PID=" + txt
            print("Message reçu decode :", txt)
            queue_espnow.append(txt)   # pas d’await ici !


"""
Main de l'application
"""

# initialisaion du Serveur
server=ServerAsync("ESP32-S3", style, script, body)
server.set_handler(http_handler)
server.set_sse_queue(queue_sse)


"""
# connexion aux robots
peer_mac = robot_mac[1]
print("peer_mac=", peer_mac)
e.add_peer(peer_mac)
"""

async def espnow_dispatcher():
    while True:
        if queue_espnow:
            print("espnow_dispatcher", queue_espnow)
            try:
                msg = queue_espnow.pop(0)

                # Exemple : "5:0.90:stop"
                # parts = msg.split(":")
                # pid = parts[0]  # "5"

                await queue_sse.put(msg)
            except:
                pass

        await asyncio.sleep(0.05)

e.irq(on_recv)

# boucle du serveur
async def main():
    queue_espnow.clear()
    # asyncio.create_task(espnow_dispatcher())
    await server.run()
    
simul_robots()

asyncio.run(main())
