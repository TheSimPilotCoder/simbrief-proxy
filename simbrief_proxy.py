from flask import Flask, jsonify, request
import requests
import xml.etree.ElementTree as ET
import os

app = Flask(__name__)

# Wake-up / Health-Check-Endpunkt
@app.route("/simbrief/health", methods=["GET"])
def health_check():
    return jsonify({"status": "Proxy ist aktiv."}), 200

# Route und Flughöhe abrufen
@app.route("/simbrief/route", methods=["GET"])
def get_route_data():
    # Standard-XML-Quelle oder benutzerdefinierte über ?xml=...
    xml_url = request.args.get("xml") or "https://www.simbrief.com/api/xml.fetcher.php?userid=559474"

    try:
        response = requests.get(xml_url, timeout=10)
        response.raise_for_status()

        root = ET.fromstring(response.content)

        # Korrekte Pfade innerhalb <general>
        route = root.findtext("./general/route_text") or "unbekannt"
        fl = root.findtext("./general/initial_altitude") or "unbekannt"

        return jsonify({
            "route": route,
            "initial_altitude": fl
        })

    except Exception as e:
        return jsonify({
            "error": "Fehler beim Abrufen der Route",
            "details": str(e)
        }), 500

# Wichtige Startkonfiguration für Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
