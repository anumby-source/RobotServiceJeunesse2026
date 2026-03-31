import network
import time
import socket
import gc
import machine

SSID = "ESP32-CAM"
PASSWORD = "12345678"
PORT = 80

class Server:
    def __init__(self, title="ESP32-S3", style="", script="", body=""):
        self.set_title(title)
        self.set_style(style)
        self.set_script(script)
        self.set_body(body)

        self.http_handler = None
        self.sse_handler = None

        self.sse_client = None   # socket du client SSE
        self.sse_active = False  # indique si un flux SSE est actif

        # WiFi AP
        self.ap = network.WLAN(network.AP_IF)
        self.ap.active(True)
        self.ap.config(essid=SSID, password=PASSWORD)

        while not self.ap.active():
            time.sleep(0.2)

        print("IP:", self.ap.ifconfig()[0])

        # Socket serveur
        self.s = socket.socket()
        try:
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        except:
            pass
        self.s.bind(("0.0.0.0", PORT))
        self.s.listen(5)
        self.s.settimeout(0.1)  # très court pour rester réactif
        self.running = False

    # -------------------------
    # Configuration
    # -------------------------

    def set_title(self, title): self.title = title
    def set_style(self, style=""): self.style = style
    def set_script(self, script=""): self.script = script
    def set_body(self, body=""): self.body = body

    def set_handler(self, func):
        self.http_handler = func

    def set_sse_handler(self, func):
        self.sse_handler = func

    # -------------------------
    # HTTP helpers
    # -------------------------

    def send_html(self, conn, html):
        conn.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n")
        conn.send(html)

    def send_text(self, conn, text):
        conn.send("HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n")
        conn.send(text)

    def send_sse_headers(self, conn):
        conn.send(b"HTTP/1.1 200 OK\r\n")
        conn.send(b"Content-Type: text/event-stream\r\n")
        conn.send(b"Cache-Control: no-cache\r\n")
        conn.send(b"Connection: keep-alive\r\n\r\n")

    # -------------------------
    # Page HTML
    # -------------------------

    def html(self):
        return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>{self.title}</title>

<style>
body {{ background:#111; color:white; text-align:center; font-family:Arial; }}
button {{ padding:10px 20px; margin:5px; font-size:15px; border:none; border-radius:8px; }}
.exit {{ background:#900; color:white; }}
.card {{ background:#222; padding:20px; border-radius:15px; display:inline-block; }}
{self.style}
</style>

</head>
<body>

<div class="card">
<h2>{self.title}</h2>
<br>{self.body}
<button class="exit" onclick="exitServer()">Exit</button>
</div>

<script>
function exitServer() {{ fetch("/exit"); }}
{self.script}
</script>

</body>
</html>
"""

    # -------------------------
    # Tick SSE (non bloquant)
    # -------------------------

    def sse_tick(self):
        """Appelé régulièrement dans run()"""
        if self.sse_handler and self.sse_client:
            try:
                self.sse_handler(self, self.sse_client)
            except:
                self.sse_client = None
                self.sse_active = False

    # -------------------------
    # Main loop
    # -------------------------

    def run(self):
        self.running = True

        while self.running:
            # Tick SSE (non bloquant)
            self.sse_tick()

            # Accept new connections
            try:
                conn, addr = self.s.accept()
            except:
                continue

            try:
                request = conn.recv(1024).decode()
                if not request:
                    conn.close()
                    continue

                method, path, _ = request.split(" ", 2)

                if path == "/exit":
                    self.running = False
                    self.stop_server()
                    break

                if path == "/events":
                    self.send_sse_headers(conn)
                    self.sse_client = conn
                    self.sse_active = True
                    continue

                if self.http_handler:
                    handled = self.http_handler(self, path, conn)
                    if handled:
                        conn.close()
                        continue

                if path == "/":
                    self.send_html(conn, self.html())
                    conn.close()
                    continue

                conn.send("HTTP/1.1 404 Not Found\r\n\r\n")
                conn.close()

            except:
                try:
                    conn.close()
                except:
                    pass

        print("BYE")

    def stop_server(self):
        self.s.close()
        self.ap.active(False)
        gc.collect()
        time.sleep(1)
        machine.reset()
