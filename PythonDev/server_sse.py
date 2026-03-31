import network
import time
import socket
import gc
import machine

SSID = "ESP32-CAM"
PASSWORD = "12345678"
PORT = 80



# =====================
# SERVER
# =====================

class Server:
    def __init__(self, title="ESP32-S3", style = "", script="", body=""):
        self.set_title(title)
        self.set_style(style)
        self.set_script(script)
        self.set_body(body)
        self.ap = network.WLAN(network.AP_IF)
        self.ap.active(True)
        self.ap.config(essid=SSID, password=PASSWORD)

        while not self.ap.active():
            time.sleep(0.2)

        print("IP:", self.ap.ifconfig()[0])

        self.s = socket.socket()
        try:
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        except:
            pass
        self.s.bind(("0.0.0.0", PORT))
        self.s.listen(5)
        self.s.settimeout(2)
        self.running = False
        self.request_handler = None
        self.sse_handler = None


    def set_title(self, title):
        self.title = title

    def set_style(self, style=""):
        self.style = style

    def set_script(self, script=""):
        self.script = script

    def set_body(self, body=""):
        self.body = body

    def stop_server(self):
        self.s.close()
        self.ap.active(False)
        gc.collect()
        time.sleep(1)
        machine.reset()


    def html(self):
        return """HTTP/1.1 200 OK
               Content-Type: text/html
               <!DOCTYPE html>
               <html>
               <head>
               <meta charset='utf-8'>
               <title>""" + self.title + """</title>
               <style>
                   body { background:#111; color:white; text-align:center; font-family:Arial; }
                   button { padding:10px 20px; margin:5px; font-size:15px; border:none; border-radius:8px; }
                   .exit { background:#900; color:white; }
                   .card { background:#222; padding:20px; border-radius:15px; display:inline-block; }
                   input { padding:5px; font-size:16px; width:80px; }
                   .running { color:orange; font-weight:bold; }
               """ + self.style + """
               </style>
               <script>
                   function runstart()
                       const eventSource = new EventSource('/sse');
                       eventSource.onmessage = function(e) {
                           document.getElementById('messages').innerHTML += e.data + '<br>';
                       };
                   }
               """ + self.script + """
               </script>
               </head>
               <body>
               <div class='card'>
               <h1>""" + self.title + """</h1>
               <div id='messages'></div>
               <button class='start' onclick='runstart()'>Start</button>
               </div>
               </body>
               </html>"""


    #     <button class="exit" onclick="testServer()">Test</button>

    def set_request_handler(self, handler):
        self.request_handler = handler

    def set_sse_handler(self, handler):
        """Définit une fonction génératrice pour les données SSE.
           La fonction doit être un générateur (yield)."""
        self.sse_handler = handler

    def handle_request(self, request):
        """Gère les requêtes HTTP classiques et SSE."""
        if request.startswith("GET /sse"):
            return self._handle_sse(request)
        else:
            return self._handle_normal_request(request)

    def _handle_sse(self, request):
        """Gère une requête SSE."""
        response = """HTTP/1.1 200 OK
                    Content-Type: text/event-stream
                    Cache-Control: no-cache
                    Connection: keep-alive"""
        return response, self.sse_handler
        # return "\r\n".join(response), self.sse_handler


    def _handle_normal_request(self, request):
        """Gère une requête HTTP classique."""
        if "GET /exit" in request:
            self.running = False

            print("server> exit")

            self.stop_server()
            return "HTTP/1.1 200 OK\r\n\r\nBYE", None

        # elif "GET /test" in request:
        #     conn.send("HTTP/1.1 200 OK\r\n\r\nTEST")

        elif "GET / " in request:
            response = self.html()

        else:
            response = "HTTP/1.1 404 Not Found\r\n\r\n"

        return response, None
        # return "\r\n".join(response), None



    def run(self):
        self.running = True
        while self.running:
            try:
                conn, addr = self.s.accept()
            except OSError:
                continue

            try:
                request = conn.recv(1024).decode()
                response, handler = self.handle_request(request)
                conn.send(response.encode())

                # Si c'est une requête SSE, on envoie les données en continu
                if handler:
                    try:
                        for data in handler():
                            conn.send(f"data: {data}\n\n".encode())
                            time.sleep(1)  # Délai entre chaque envoi
                    except OSError:
                        # Le client a fermé la connexion
                        pass
                    finally:
                        conn.close()
                else:
                    conn.close()

            except Exception as e:
                print("Erreur:", e)
                try:
                    conn.close()
                except:
                    pass

        print("BYE")


