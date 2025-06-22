from flask import Flask, jsonify, request
import requests
import xml.etree.ElementTree as ET
import os

app = Flask(__name__)

# Health-Check Endpoint zum "Aufwecken"
@app.route("/simbrief/health", methods=["GET"])
def health_check():
    return jsonify({"status": "Proxy ist aktiv."}), 200

# Route-Endpunkt (liefert Route + Flughöhe)
@app.route("/simbrief/route", methods=["GET"])
def get_route_data():
    xml_url = request.args.get("xml") or "https://www.simbrief.com/api/xml.fetcher.php?userid=559474"

    try:
        response = requests.get(xml_url)
        response.raise_for_status()

        root = ET.fromstring(response.content)
        route = root.findtext("route_text") or "unbekannt"
        fl = root.findtext("initial_altitude") or "unbekannt"

        return jsonify({
            "route": route,
            "initial_altitude": fl
        })

    except Exception as e:
        return jsonify({
            "error": "Fehler beim Abrufen der Route",
            "details": str(e)
        }), 500

# Wichtig für Render: richtige Host/Port-Konfiguration
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
