from flask import Flask, Response
import requests

app = Flask(__name__)

# Deine SimBrief-User-ID – falls du mal ändern willst, einfach hier anpassen
SIMBRIEF_USER_ID = "559474"

@app.route("/simbrief/ofp", methods=["GET"])
def get_simbrief_ofp():
    url = f"https://www.simbrief.com/api/xml.fetcher.php?userid={SIMBRIEF_USER_ID}"
    simbrief_response = requests.get(url)

    if simbrief_response.status_code == 200:
        return Response(simbrief_response.content, mimetype="application/xml")
    else:
        return Response("Fehler beim Abruf des SimBrief-Flugplans", status=500)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
