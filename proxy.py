import json
import urllib.parse
import base64
from mitmproxy import http

# Načtení konfigurace
CONFIG_FILE = "/etc/mitmproxy/config.json"
with open(CONFIG_FILE, "r", encoding="utf-8") as f:
    config = json.load(f)

def request(flow: http.HTTPFlow):
    """ Přidá přihlašovací údaje do požadavků """
    url_path = flow.request.path
    decoded_url = urllib.parse.unquote(url_path)

    auth_config = config.get("auth", {})
    for protected_path in auth_config:
        if decoded_url.startswith(protected_path):
            username = auth_config[protected_path]["username"]
            password = auth_config[protected_path]["password"]
            auth_string = f"{username}:{password}"
            encoded_auth = base64.b64encode(auth_string.encode()).decode()

            # Přidání Authorization hlavičky
            flow.request.headers["Authorization"] = f"Basic {encoded_auth}"
            print(f"🔒 Přidán Authorization header pro {decoded_url}")

def response(flow: http.HTTPFlow):
    """ Modifikuje odpověď a přidává CSS pro posunutí """
    url_path = flow.request.path
    decoded_url = urllib.parse.unquote(url_path)

    mappings = config.get("mappings", {})

    if decoded_url in mappings:
        offsets = mappings[decoded_url]
        offset_x = offsets.get("offset_x", 0)
        offset_y = offsets.get("offset_y", 0)

        if "text/html" in flow.response.headers.get("content-type", ""):
            html = flow.response.text
            css = f"<style>body {{ transform: translate({offset_x}px, {offset_y}px); }}</style>"
            html = html.replace("</head>", css + "</head>")
            flow.response.text = html
            print(f"✏️ Modifikován obsah pro {decoded_url}: Posun {offset_x}px, {offset_y}px")

# Spuštění přes mitmdump:
# mitmdump -s proxy.py --mode reverse:http://192.168.222.104

# proxy je dostupný na adrese stroje kde se spouští na portu :8080


