import server
import re
import time

s = server.Server("ABCD")

# s.set_style(""".start { background:green; color:white; }""")

#s.set_script("""    // Le script est déjà inclus dans la méthode html()""")

# s.set_body("""<!-- Le corps est déjà inclus dans la méthode html() -->""")

def sse_data_generator():
    """Générateur de données pour les SSE."""
    for i in range(10):
        yield f"Message {i}"
        time.sleep(1)

def handle_request(server, request, conn):
    m = re.match(r"GET ([^ ]*) HTTP", request)
    if not m:
        conn.send("HTTP/1.1 400 Bad Request\r\n\r\n")
        return False

    path = m.group(1)
    print("Request path:", path)

    if path == "/start":
        print("START")
        response = """HTTP/1.1 200 OK
                   Content-Type: text/html
                   """
        conn.send(response)
        # conn.send(server.html().split("\r\n", 3)[-1])
        conn.send(server.html())
        conn.close()
        return True

    return False

s.set_request_handler(handle_request)
# s.set_sse_handler(sse_data_generator)

s.run()
