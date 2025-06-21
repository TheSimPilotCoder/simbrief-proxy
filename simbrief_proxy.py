from flask import Flask, jsonify
import requests
import xml.etree.ElementTree as ET

app = Flask(__name__)

SIMBRIEF_USER_ID = "559474"
SIMBRIEF_URL = f"https://www.simbrief.com/api/xml.fetcher.php?userid={SIMBRIEF_USER_ID}"

def get_xml_root():
    response = requests.get(SIMBRIEF_URL)
    if response.status_code != 200:
        return None
    root = ET.fromstring(response.content)
    return root

@app.route("/simbrief/route", methods=["GET"])
def get_route():
    root = get_xml_root()
    if root is None:
        return jsonify({"error": "Flugplan konnte nicht abgerufen werden"}), 500

    route = root.findtext("general/route")
    atc_route = root.findtext("general/atcroute")
    altitudes = root.findtext("general/initial_altitude")

    return jsonify({
        "icao_route": route,
        "atc_route": atc_route,
        "initial_altitude": altitudes
    })

@app.route("/simbrief/weather", methods=["GET"])
def get_weather():
    root = get_xml_root()
    if root is None:
        return jsonify({"error": "Flugplan konnte nicht abgerufen werden"}), 500

    metar_dep = root.findtext("weather/origin/metar")
    metar_arr = root.findtext("weather/destination/metar")
    taf_dep = root.findtext("weather/origin/taf")
    taf_arr = root.findtext("weather/destination/taf")

    return jsonify({
        "departure_metar": metar_dep,
        "arrival_metar": metar_arr,
        "departure_taf": taf_dep,
        "arrival_taf": taf_arr
    })

@app.route("/simbrief/fuel", methods=["GET"])
def get_fuel():
    root = get_xml_root()
    if root is None:
        return jsonify({"error": "Flugplan konnte nicht abgerufen werden"}), 500

    fuel_data = root.find("fuel")
    if fuel_data is None:
        return jsonify({"error": "Fuel-Daten nicht gefunden"}), 500

    return jsonify({
        "taxi_fuel": fuel_data.findtext("taxi"),
        "trip_fuel": fuel_data.findtext("trip"),
        "contingency_fuel": fuel_data.findtext("contingency"),
        "alternate_fuel": fuel_data.findtext("alternate"),
        "final_reserve_fuel": fuel_data.findtext("final_reserve"),
        "block_fuel": fuel_data.findtext("block")
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
