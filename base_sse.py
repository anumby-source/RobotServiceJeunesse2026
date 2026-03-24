import json  # Ajout de l'import manquant
from server import Server
import espnow

# Initialisation du serveur
server = Server()

# Variable globale pour stocker l'état des images sélectionnées
selected_images = {i: False for i in range(1, 8)}

# Liste des noms des images dans l'ordre
image_names = [
    "stop.png",
    "cedez_le_passage.png",
    "priorite_a_droite.png",
    "pietons.png",
    "rond_point.png",
    "stationnement.png",
    "start.png"
]

# Liste des clients SSE
sse_clients = []

def serve_static_file(path):
    try:
        with open("static/" + path.split('/')[-1], "rb") as file:
            content = file.read()
        content_type = "image/png"  # Tous les fichiers servis ici sont des PNG
        return ("HTTP/1.1 200 OK\r\nContent-Type: {}\r\n\r\n".format(content_type), [content])
    except OSError:
        print(f"Fichier non trouvé : {path}")
        return ("HTTP/1.1 404 Not Found\r\n\r\n", [])

def request_handler(request):
    path = request["path"]
    if path == "/":
        return render_main_page()
    elif path == "/sse":
        return handle_sse(request)
    elif path == "/reset":
        reset_images()
        return ("HTTP/1.1 303 See Other\r\nLocation: /\r\n\r\n", [])
    elif path.startswith("/static/"):
        return serve_static_file(path)
    else:
        return ("HTTP/1.1 404 Not Found\r\n\r\n", [])

def render_main_page():
    html = server.set_body(render_html())
    css = server.set_style(render_css())
    js = server.set_script(render_js())
    return ("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + html + css + js, [])

def render_html():
    return """
        <h1>Image Selector</h1>
        <div id="images-container">
            <!-- Les images seront ajoutées ici par JavaScript -->
        </div>
        <button id="reset-button">Réinitialiser</button>
    """

def render_css():
    return """
        #images-container {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }
        .image-item {
            border: 2px solid transparent;
            padding: 5px;
        }
        .selected {
            border: 2px solid red;
        }
        img {
            width: 100px;
            height: 100px;
        }
    """

def render_js():
    return f"""
        const imagesContainer = document.getElementById('images-container');
        const resetButton = document.getElementById('reset-button');
        const imageNames = {json.dumps(image_names)};  # Utilisation de json.dumps pour une conversion sécurisée

        function initImages() {{
            for (let i = 0; i < imageNames.length; i++) {{
                const imgItem = document.createElement('div');
                imgItem.className = 'image-item';
                imgItem.id = `image-${{i+1}}`;
                imgItem.innerHTML = `<img src='/static/${{imageNames[i]}}' alt='Image ${{i+1}}'>`;
                imagesContainer.appendChild(imgItem);
            }}
        }}

        resetButton.addEventListener('click', () => {{
            fetch('/reset', {{ method: 'POST' }});
        }});

        const eventSource = new EventSource('/sse');
        eventSource.onmessage = (event) => {{
            const data = JSON.parse(event.data);
            if (data.action === 'select') {{
                const imgItem = document.getElementById(`image-${{data.id}}`);
                imgItem.classList.add('selected');
            }} else if (data.action === 'reset') {{
                document.querySelectorAll('.image-item').forEach(item => {{
                    item.classList.remove('selected');
                }});
            }}
        }};

        window.onload = initImages;
    """

def handle_sse(request):
    client = request["client"]
    sse_clients.append(client)

    def on_close():
        sse_clients.remove(client)

    client.on_close(on_close)
    client.send("data: " + json.dumps({"action": "reset"}) + "\n\n")
    return ("", [])

def send_sse_event(action, id=None):
    event = {"action": action}
    if id is not None:
        event["id"] = id
    for client in sse_clients:
        client.send("data: " + json.dumps(event) + "\n\n")

def on_espnow_receive(mac, msg):
    try:
        msg = msg.decode('utf-8')
        if msg.startswith("select:"):
            image_name = msg.split(":")[1]
            if image_name in image_names:
                image_id = image_names.index(image_name) + 1
                selected_images[image_id] = True
                send_sse_event("select", image_id)
            else:
                print(f"Image non trouvée : {image_name}")
    except Exception as e:
        print(f"Erreur lors de la réception du message ESP-NOW : {e}")

def reset_images():
    for i in range(1, 8):
        selected_images[i] = False
    send_sse_event("reset")

# Initialisation d'ESP-NOW
e = espnow.ESPNow()
e.active(True)
e.add_peer(b'\xFF\xFF\xFF\xFF\xFF\xFF')  # Adresse MAC de diffusion
# e.set_pmk(b'PMK_KEY_1234567890ABC')  # Décommentez si vous utilisez une clé PMK
e.on_receive(on_espnow_receive)

# Lancement du serveur
server.run(request_handler)
