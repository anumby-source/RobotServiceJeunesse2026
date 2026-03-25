import uasyncio as asyncio
import urandom
from server_async import ServerAsync
from simple_queue import SimpleQueue
import time

from mac_addr import *
import espnow

# Initialisation d’ESP-NOW
e = espnow.ESPNow()
e.active(True)

esp_task = None

q=SimpleQueue()
irq_queue = []

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
    
jeu = Jeu()

async def http_handler(server, path, w):
    global esp_task
    
    print("http_handler", path, jeu.running)
    if path.startswith("/btn/"):
        n = path.split("/")[-1]
        print("http_handler> BTN=", n)
        if n == '6':
            jeu.start()
        elif n == '7':
            jeu.stop()

        if jeu.running or n == '7':
            t = jeu.now()
            p = len(jeu.penalties)
            total = t + p
            values = f"VALUES={t},{p},{total}"
            print("values=", values)
            await q.put(values)
            await q.put("BTN=" + n)
        await w.awrite("HTTP/1.1 200 OK\r\n\r\nOK")
        await w.aclose()
        
        print("jeu btn", jeu.running)
        return True

    if path.startswith("/start"):
        await q.put("START")
        # esp_task = asyncio.create_task(espnow_sim())
        # esp_task = asyncio.create_task(callback(e))
        await w.awrite("HTTP/1.1 200 OK\r\n\r\nOK")
        await w.aclose()
        jeu.restart()
        print("jeu START", jeu.running)
        return True

    if path=="/reset":
        await q.put("RESET")
        if not esp_task is None:
            esp_task.cancel()
        jeu.reset()
        values = f"VALUES=0,0,0"
        print("values=", values)
        await q.put(values)
        await w.awrite("HTTP/1.1 200 OK\r\n\r\nOK")
        await w.aclose()
        print("jeu RESET", jeu.running)
        return True

    return False


def callback(e):
    # Attendre un message
    mac, msg = e.recv()
    if msg:  # Si un message est reçu        
        txt = msg.decode('utf-8')
        print("Message reçu decode :", txt)
        irq_queue.append(txt)   # pas d’await ici !

async def espnow_dispatcher():
    while True:
        if irq_queue:
            print("espnow_dispatcher", irq_queue)
            try:
                msg = irq_queue.pop(0)

                # Exemple : "5:0.90:stop"
                # parts = msg.split(":")
                # pid = parts[0]  # "5"

                await q.put("PID=" + msg)
            except:
                pass

        await asyncio.sleep(0.05)

async def espnow_sim():
    while True:
        await asyncio.sleep(2)
        n=urandom.getrandbits(3)%7+1
        await q.put("PID="+str(n))

style=(
".g{margin-top:10px;display:flex;flex-direction:column;align-items:center;}"
".g table {margin:auto;}"
".g button{padding:10px;font-size:15px;background:green;color:#fff;border:none;border-radius:8px;}"
".log{margin-top:10px;max-height:150px;overflow:auto;font-family:monospace;}"
".status{font-size:15px;background:#ECECB9;color: black;display:inline-block;}"
".value{padding:5px;font-size:20px;color:red;max-height:20px;resize:none;overflow:hidden;"
"}"
)

body=(
        "<button id='startBtn' onclick=fetch('/start');>START</button>"
        "<button id='resetBtn' onclick=fetch('/reset');>RESET</button>"
        "<div class='g'>"
                "<table>"
                        "<tr>"
                                "<td>"
                                        "<button id='b6' onclick=p(6);>Start</button>"
                                "</td>"
                        "</tr>"
                        "<tr>"
                                "<td>"
                                        "<button id='b1' onclick=p(1);>Limite 30</button>"
                                        "<button id='b2' onclick=p(2);>Cedez le passage</button>"
                                        "<button id='b3' onclick=p(3);>Passage pietons</button>"
                                        "<button id='b4' onclick=p(4);>Priorite a droite</button>"
                                        "<button id='b5' onclick=p(5);>Stationnement</button>"
                                "</td>"
                        "</tr>"
                        "<tr>"
                                "<td>"
                                        "<button id='b7' onclick=p(7);>Stop</button>"
                                "</td>"
                        "</tr>"
                "</table>"
        "</div>"
        "<div id='status' class='status'>"
                "<p>Jeu</p>"
                "<table>"
                        "<tr>"
                                "<td>temps ecoule:</td><td><textarea id='t1' class='value'>t1</textarea></td>"
                                "<td>penalites:</td><td><textarea id='t2' class='value'>t2</textarea></td>"
                                "<td>temps total:</td><td><textarea id='t3' class='value'>t3</textarea></td>"
                        "</tr>"
                "</table>"
        "</div>"
        "<div id='log' class='log'>"
        "</div>"
)

script=(
        "var L = document.getElementById('log');"
        "var E = new EventSource('/events');"
        "function p(i){fetch('/btn/'+i);}"
        "window.p = p;"
        "function RB(){"
            "for(let i=1;i<=7;i++) document.getElementById('b'+i).style.background='green';"
        "}"
        "function sendVal(t) {"
            "const v = document.getElementById(t).value;"
            "fetch('/set?value=' + encodeURIComponent(v));"
        "}"
        "E.onmessage=function(e){"
            "var m = e.data;"
            "console.log(m);"
            "var ligne = document.createElement('p');"
            "ligne.textContent = m;"
            "L.appendChild(ligne);"
            "if (m == 'RESET') {RB();return;}"
            "if (m.startsWith('PID=')) {"
              "var n = parseInt(m.substring(4));"
              "console.log(n);"
              # "RB();"
              "document.getElementById('b'+m).style.background='red';"
            "}"
            "if (m.startsWith('BTN=')) {"
              "var n = parseInt(m.substring(4));"
              "console.log(n);"
              # "RB();"
              "document.getElementById('b'+n).style.background='red';"
            "}"
            "if (m.startsWith('VALUES=')) {"
                "const parts = m.substring(7).split(',');"
                "document.getElementById('t1').value = parts[0] || '';"
                "document.getElementById('t2').value = parts[1] || '';"
                "document.getElementById('t3').value = parts[2] || '';"
            "}"


        "};"

)

server=ServerAsync("ESP32-S3", style, script, body)
server.set_handler(http_handler)
server.set_sse_queue(q)

peer_mac = robot_mac[1]
print("peer_mac=", peer_mac)
e.add_peer(peer_mac)

e.irq(callback)

async def main():
    irq_queue.clear() 
    asyncio.create_task(espnow_dispatcher())
    await server.run()

asyncio.run(main())


