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

queue_sse = SimpleQueue()
queue_espnow = []

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
    
jeuA = Jeu()
jeuB = Jeu()

async def http_handler(server, path, w):
    global esp_task
    
    print("http_handler", path, jeuA.running, jeuB.running)
    if path.startswith("/Abtn/"):
        n = path.split("/")[-1]
        print("http_handler> ABTN=", n)
        if n == '6':
            jeuA.start()
        elif n == '7':
            jeuA.stop()

        if jeuA.running or n == '7':
            t = jeuA.now()
            p = len(jeuA.penalties)
            total = t + p
            values = f"AVALUES={t},{p},{total}"
            print("values=", values)
            await queue_sse.put(values)
            await queue_sse.put("ABTN=" + n)
        await w.awrite("HTTP/1.1 200 OK\r\n\r\nOK")
        await w.aclose()
        
        print("jeu btn", jeuA.running)
        return True

    if path.startswith("/Bbtn/"):
        n = path.split("/")[-1]
        print("http_handler> BBTN=", n)
        if n == '6':
            jeuB.start()
        elif n == '7':
            jeuB.stop()

        if jeuB.running or n == '7':
            t = jeuB.now()
            p = len(jeuB.penalties)
            total = t + p
            values = f"BVALUES={t},{p},{total}"
            print("values=", values)
            await queue_sse.put(values)
            await queue_sse.put("BBTN=" + n)
        await w.awrite("HTTP/1.1 200 OK\r\n\r\nOK")
        await w.aclose()
        
        print("jeuB btn", jeuB.running)
        return True

    if path.startswith("/start"):
        await queue_sse.put("START")
        # esp_task = asyncio.create_task(espnow_sim())
        # esp_task = asyncio.create_task(callback(e))
        await w.awrite("HTTP/1.1 200 OK\r\n\r\nOK")
        await w.aclose()
        jeuA.restart()
        jeuB.restart()
        print("jeu START", jeuA.running, jeuB.running)
        return True

    if path=="/reset":
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
        return True

    return False


def callback(e):
    # Attendre un message
    mac, msg = e.recv()
    if msg:  # Si un message est reçu        
        txt = msg.decode('utf-8')
        print("Message reçu decode :", txt)
        queue_espnow.append(txt)   # pas d’await ici !

async def espnow_dispatcher():
    while True:
        if queue_espnow:
            print("espnow_dispatcher", queue_espnow)
            try:
                msg = queue_espnow.pop(0)

                # Exemple : "5:0.90:stop"
                # parts = msg.split(":")
                # pid = parts[0]  # "5"

                await queue_sse.put("PID=" + msg)
            except:
                pass

        await asyncio.sleep(0.05)

async def espnow_sim():
    while True:
        await asyncio.sleep(2)
        n=urandom.getrandbits(3)%7+1
        await queue_sse.put("PID="+str(n))

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
"<h2>" + side + "</h2>"
"<div class='g'>"
"<table><tr>"
"<td>"
"<button id='" + side + "b6' onclick=" + side + "p(6);>Start</button>"
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
                                        "<button id='" + side + "b7' onclick=" + side + "p(7);>Stop</button>"
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

def script_side(side):
    return (
            "if (key === '" + side + "PID') {"
              "var n = obj;"
              "console.log(n);"
              # "" + side + "RB();"
              "document.getElementById('" + side + "b'+m).style.background='red';"
              "" + side + "L.appendChild(ligne);"
            "}"
            "if (key === '" + side + "BTN') {"
              "var n = obj;"
              "console.log(n);"
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
        "E.onmessage=function(e){"
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

server=ServerAsync("ESP32-S3", style, script, body)
server.set_handler(http_handler)
server.set_sse_queue(queue_sse)

peer_mac = robot_mac[1]
print("peer_mac=", peer_mac)
e.add_peer(peer_mac)

e.irq(callback)

async def main():
    queue_espnow.clear()
    asyncio.create_task(espnow_dispatcher())
    await server.run()

asyncio.run(main())
