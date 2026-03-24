import uasyncio as asyncio
import urandom
from server_async import ServerAsync
from simple_queue import SimpleQueue

esp_task = None

q=SimpleQueue()

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
        esp_task = asyncio.create_task(espnow_sim())
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

#        "function s(){fetch('/start');}"
#        "function r(){fetch('/reset');}"
#        "function exitServer(){fetch('/exit');}"
#
#        "window.s=s;"
#        "window.r=r;"
#        "window.p=p;"
#        "window.exitServer=exitServer;"


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
              "document.getElementById('b'+n).style.background='red';}"
        "};"

)

server=ServerAsync("ESP32-S3", style, script, body)
server.set_handler(http_handler)
server.set_sse_queue(q)

async def main():
    await server.run()

asyncio.run(main())
