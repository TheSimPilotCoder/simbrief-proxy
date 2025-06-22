from flask import Flask, jsonify, request
import requests
import xml.etree.ElementTree as ET
import os

app = Flask(__name__)

@app.route("/simbrief/health", methods=["GET"])
def health_check():
    return jsonify({"status": "Proxy ist aktiv."}), 200

@app.route("/simbrief/route", methods=["GET"])
def get_route_data():
    xml_url = request.args.get("xml") or "https://www.simbrief.com/api/xml.fetcher.php?userid=559474"

    try:
        response = requests.get(xml_url, timeout=10)
        response.raise_for_status()

        root = ET.fromstring(response.content)
        general = root.find("general")
        if general is None:
            return jsonify({"error": "Kein <general>-Block im XML gefunden."}), 500

        fl = general.findtext("initial_altitude") or "unbekannt"
        route = general.findtext("route_text") or general.findtext("route_ifr") or "unbekannt"

        return jsonify({
            "route": route.strip(),
            "initial_altitude": fl.strip()
        })

    except Exception as e:
        return jsonify({
            "error": "Fehler beim Abrufen der Route",
            "details": str(e)
        }), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
