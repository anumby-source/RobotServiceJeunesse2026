import uasyncio as asyncio
import urandom
from server_async import ServerAsync
from simple_queue import SimpleQueue

from mac_addr import *
import espnow

# Initialisation d’ESP-NOW
e = espnow.ESPNow()
e.active(True)

esp_task = None

q=SimpleQueue()
irq_queue = []

async def http_handler(server, path, w):
    global esp_task
    
    print("http_handler", path)
    if path.startswith("/btn/"):
        n=path.split("/")[-1]
        await q.put("BTN="+n)
        await w.awrite("HTTP/1.1 200 OK\r\n\r\nOK")
        await w.aclose()
        return True

    if path.startswith("/start"):
        await q.put("START")
        # esp_task = asyncio.create_task(espnow_sim())
        # esp_task = asyncio.create_task(callback())
        await w.awrite("HTTP/1.1 200 OK\r\n\r\nOK")
        await w.aclose()
        return True

    if path=="/reset":
        await q.put("RESET")
        esp_task.cancel()
        await w.awrite("HTTP/1.1 200 OK\r\n\r\nOK")
        await w.aclose()
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

body=(
    "<button id='startBtn' onclick=fetch('/start');>START</button>"
    "<button id='resetBtn' onclick=fetch('/reset');>RESET</button>"
    '<div class="g">'
        "<button id='b6' onclick=p(6);>Start</button>"
        "<button id='b1' onclick=p(1);>Limite 30</button>"
        "<button id='b2' onclick=p(2);>Cdez le passage</button>"
        "<button id='b3' onclick=p(3);>Passage pietons</button>"
        "<button id='b4' onclick=p(4);>Priorite a droite</button>"
        "<button id='b5' onclick=p(5);>Stationnement</button>"
        "<button id='b7' onclick=p(7);>Stop</button>"
    '</div>'
    '<div id="log" style="margin-top:10px;max-height:150px;overflow:auto;font-family:monospace;"></div>'
)

style=(
    ".g{margin-top:10px;display:grid;grid-template-columns:repeat(4,1fr);gap:5px;}"
    ".g button{padding:10px;font-size:18px;background:green;color:#fff;border:none;border-radius:8px;}"
)



script=(
        "var L = document.getElementById('log');"
        "var E = new EventSource('/events');"

        "function p(i){fetch('/btn/'+i);}"
        "window.p=p;"

        "function RB(){"
            "for(let i=1;i<=7;i++) document.getElementById('b'+i).style.background='green';"
        "}"

        "E.onmessage=function(e){"
            "var m = e.data;"
            "var p = document.createElement('p');"
            "p.textContent = m;"
            "L.appendChild(p);"
            "if (m == 'RESET') {RB();return;}"
            "if (m.startsWith('PID=')) {"
              "var n=parseInt(m.substring(4));"
              # "RB();"
              "document.getElementById('b'+m).style.background='red';}"
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
