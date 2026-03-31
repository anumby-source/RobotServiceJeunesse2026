from server import Server
import time

start_flag = False
counter = 0

# -------------------------
# Handler HTTP normal
# -------------------------

def http_handler(server, path, conn):
    global start_flag

    if path == "/start":
        start_flag = True
        server.send_text(conn, "OK")
        return True

    return False

# -------------------------
# Handler SSE non bloquant
# -------------------------

def sse_handler(server, conn):
    global start_flag, counter

    if start_flag:
        start_flag = False
        counter = 1

    if counter > 0 and counter <= 10:
        conn.send(f"data: Message {counter}\n\n")
        counter += 1
        time.sleep(1)

    if counter > 10:
        counter = 0  # fin de séquence

# -------------------------
# IHM
# -------------------------

body = """
<button onclick="start()">Start</button>
<div id="log" style="margin-top:20px; text-align:left; max-height:200px; overflow:auto; font-family:monospace;"></div>
"""

script = """
function start() {
    fetch('/start');
}

const log = document.getElementById("log");
const evt = new EventSource('/events');

evt.onmessage = (event) => {
    const p = document.createElement("p");
    p.textContent = event.data;
    log.appendChild(p);
};
"""

style = """
"""

# -------------------------
# Serveur
# -------------------------

s = Server(title="SSE Demo ESP32-S3")
s.set_body(body)
s.set_style(style)
s.set_script(script)
s.set_handler(http_handler)
s.set_sse_handler(sse_handler)
s.run()
