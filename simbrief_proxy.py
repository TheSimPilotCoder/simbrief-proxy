from flask import Flask, jsonify, request
import requests
import xml.etree.ElementTree as ET

app = Flask(__name__)

@app.route("/simbrief/route", methods=["GET"])
def get_route_data():
    xml_url = request.args.get("xml") or "https://www.simbrief.com/api/xml.fetcher.php?userid=559474"

    try:
        response = requests.get(xml_url)
        response.raise_for_status()

        # XML parsen
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
