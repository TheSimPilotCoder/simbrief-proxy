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

    def clean(text):
        return text if text and "No valid" not in text else None

    metar_dep = clean(root.findtext("origin/metar"))
    taf_dep = clean(root.findtext("origin/taf"))
    metar_arr = clean(root.findtext("destination/metar"))
    taf_arr = clean(root.findtext("destination/taf"))

    # Alternate ebenfalls extrahieren
    alt_code = root.findtext("alternate/icao_code")
    metar_alt = clean(root.findtext("alternate/metar"))
    taf_alt = clean(root.findtext("alternate/taf"))

    return jsonify({
        "departure_metar": metar_dep or "Kein gültiger METAR vorhanden",
        "departure_taf": taf_dep or "Kein gültiger TAF vorhanden",
        "arrival_metar": metar_arr or "Kein gültiger METAR vorhanden",
        "arrival_taf": taf_arr or "Kein gültiger TAF vorhanden",
        "alternate": {
            "icao": alt_code,
            "metar": metar_alt or "Kein gültiger METAR vorhanden",
            "taf": taf_alt or "Kein gültiger TAF vorhanden"
        }
    })

@app.route("/simbrief/fuel", methods=["GET"])
def get_fuel():
    root = get_xml_root()
    if root is None:
        return jsonify({"error": "Flugplan konnte nicht abgerufen werden"}), 500

    fuel = root.find("fuel")
    if fuel is None:
        return jsonify({"error": "Fuel-Daten nicht gefunden"}), 500

    return jsonify({
        "taxi": fuel.findtext("taxi"),
        "trip": fuel.findtext("enroute_burn"),
        "contingency": fuel.findtext("contingency"),
        "alternate": fuel.findtext("alternate_burn"),
        "final_reserve": fuel.findtext("reserve"),
        "min_takeoff": fuel.findtext("min_takeoff"),
        "plan_takeoff": fuel.findtext("plan_takeoff"),
        "plan_ramp": fuel.findtext("plan_ramp"),
        "plan_landing": fuel.findtext("plan_landing"),
        "avg_fuel_flow": fuel.findtext("avg_fuel_flow")
    })


@app.route("/simbrief/weights", methods=["GET"])
def get_weights():
    root = get_xml_root()
    if root is None:
        return jsonify({"error": "Flugplan konnte nicht abgerufen werden"}), 500

    w = root.find("weights")
    if w is None:
        return jsonify({"error": "Gewichtsdaten nicht gefunden"}), 500

    return jsonify({
        "pax_count": w.findtext("pax_count"),
        "bag_count": w.findtext("bag_count"),
        "payload": w.findtext("payload"),
        "cargo": w.findtext("cargo"),
        "est_zfw": w.findtext("est_zfw"),
        "est_tow": w.findtext("est_tow"),
        "est_ldw": w.findtext("est_ldw"),
        "max_zfw": w.findtext("max_zfw"),
        "max_tow": w.findtext("max_tow"),
        "max_ldw": w.findtext("max_ldw"),
        "est_ramp": w.findtext("est_ramp")
    })


@app.route("/simbrief/times", methods=["GET"])
def get_times():
    root = get_xml_root()
    if root is None:
        return jsonify({"error": "Flugplan konnte nicht abgerufen werden"}), 500

    t = root.find("times")
    if t is None:
        return jsonify({"error": "Zeitdaten nicht gefunden"}), 500

    return jsonify({
        "sched_out": t.findtext("sched_out"),
        "sched_off": t.findtext("sched_off"),
        "sched_on": t.findtext("sched_on"),
        "sched_in": t.findtext("sched_in"),
        "est_out": t.findtext("est_out"),
        "est_off": t.findtext("est_off"),
        "est_on": t.findtext("est_on"),
        "est_in": t.findtext("est_in"),
        "est_block": t.findtext("est_block"),
        "taxi_out": t.findtext("taxi_out"),
        "taxi_in": t.findtext("taxi_in"),
        "reserve_time": t.findtext("reserve_time"),
        "endurance": t.findtext("endurance")
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
