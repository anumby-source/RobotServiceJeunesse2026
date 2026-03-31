import uasyncio as asyncio
import network
import machine

SSID="ESP32-CAM"
PASSWORD="12345678"
PORT=80

class ServerAsync:
    def __init__(self,title="",style="",script="",body=""):
        self.title=title
        self.style=style
        self.script=script
        self.body=body
        self.http_handler=None
        self.sse_queue=None
        self.sse_clients=[]

    def set_handler(self,h): self.http_handler=h
    def set_sse_queue(self,q): self.sse_queue=q

    def html(self):
        return (
"<!DOCTYPE html>"
"<html>"
"<head>"
"<meta charset='utf-8'>"
"<title>"

+ self.title +

"</title>"
"<style>"
"body{background:#111;color:#fff;display: flex;text-align:center;justify-content: center;align-items: center;font-family:Arial;}"
"button{padding:10px 20px;margin:5px;font-size:15px;border:none;border-radius:8px;}"
".exit{background:#900;color:#fff;}"
".card{background:#222;padding:20px;border-radius:15px;flex-direction:column;gap:15px;align-items:center;}"

+ self.style +

"</style>"
"</head>"
"<body>"
"<div class='card'>"
"<h2>"

+ self.title +

"</h2>"

+ self.body +

"<button class='exit' id='exitBtn' onclick=fetch('/exit');>Exit</button>"
"</div>"
"<script>"

+ self.script +

"</script>"
"</body></html>"
        )

    async def send_html(self,writer):
        """
        page = self.html()
        print("Server.send_html", len(page))

        header = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html\r\n"
            "Connection: close\r\n"
            "\r\n"
        )

        await writer.awrite(header)

        bloc = 1024
        for i in range(0, len(page), bloc):
            b = page[i:i+bloc]
            print("Server.send_html", len(b))
            await writer.awrite(b)

            # flush si disponible
            if hasattr(writer, "drain"):
                await writer.drain()
            else:
                await asyncio.sleep_ms(1)

        await writer.aclose()
        """
        page=self.html()
        # print("Server.send_html> page=", len(page))

        header="HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"

        await writer.awrite(header)
        await asyncio.sleep(0)

        bloc = 1024*8
        for i in range(0, len(page), bloc):
            b = page[i:i+bloc]
            # print("Server.send_html> bloc=", len(b))
            await writer.awrite(b)
            await asyncio.sleep(0)

        await writer.aclose()

    async def sse_broadcaster(self):
        while True:
            msg=await self.sse_queue.get()
            dead=[]
            for w in self.sse_clients:
                try:
                    await w.awrite("data: "+msg+"\n\n")
                except:
                    dead.append(w)
            for w in dead:
                self.sse_clients.remove(w)

    async def handle_client(self,reader,writer):
        req=await reader.readline()
        if not req:
            await writer.aclose()
            return
        
        print("Server.handle_client", req)

        req=req.decode()
        method,path,_=req.split(" ",2)

        if path=="/exit":
            await writer.awrite("HTTP/1.1 200 OK\r\n\r\nBYE")
            await writer.aclose()
            machine.reset()

        if path=="/events":
            await writer.awrite(
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/event-stream\r\n"
                "Cache-Control: no-cache\r\n"
                "Connection: keep-alive\r\n\r\n"
            )
            self.sse_clients.append(writer)
            return

        if self.http_handler:
            handled=await self.http_handler(self, path, writer)
            if handled: return

        if path=="/":
            await self.send_html(writer)
            return

        await writer.awrite("HTTP/1.1 404 Not Found\r\n\r\n")
        await writer.aclose()

    async def run(self):
        ap=network.WLAN(network.AP_IF)
        ap.active(True)
        ap.config(essid=SSID,password=PASSWORD)

        while not ap.active():
            await asyncio.sleep(0.1)

        print("IP:",ap.ifconfig()[0])

        asyncio.create_task(self.sse_broadcaster())
        await asyncio.start_server(self.handle_client,"0.0.0.0",PORT)

        while True:
            await asyncio.sleep(1)
