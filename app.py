from flask import Flask, request
import os
import requests
from utils import geocode

app = Flask(__name__)
history = []


@app.get("/")
def hello_world():
    return "Bienvenue sur l'API Geo !"


@app.get("/coords/<city>")
def get_coords(city: str):
    try:
        response = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={"q": city, "format": "json", "limit": 1},
            headers={"User-Agent": "api-geo/1.0 (student project)"},
            timeout=10,
        )
        response.raise_for_status()
        results = response.json()
        if not results:
            return {"city": city, "error": "City not found"}, 404
        first = results[0]
        return {"city": city, "lat": float(first["lat"]), "lon": float(first["lon"])}, 200
    except requests.RequestException:
        return {"error": "Failed to contact Nominatim"}, 502


 


@app.get("/distance")
def distance():
    city_from = request.args.get("from")
    city_to = request.args.get("to")
    if not city_from or not city_to:
        return {"error": "Missing required query params: from and to"}, 400

    a = geocode(city_from)
    b = geocode(city_to)
    if not a:
        return {"error": f"City not found: {city_from}"}, 404
    if not b:
        return {"error": f"City not found: {city_to}"}, 404

    lat1, lon1 = a
    lat2, lon2 = b

    api_key = os.environ.get("OPENROUTESERVICE_API_KEY") or "eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6IjA2MjMwYjE4NjQyYTQzNmNhNmM4Njk1MTNlNTljOWUzIiwiaCI6Im11cm11cjY0In0="
    if not api_key:
        return {"error": "OPENROUTESERVICE_API_KEY is not set"}, 500

    try:
        resp = requests.get(
            "https://api.openrouteservice.org/v2/directions/driving-car",
            params={"start": f"{lon1},{lat1}", "end": f"{lon2},{lat2}"},
            headers={"Authorization": api_key},
            timeout=15,
        )
        resp.raise_for_status()
        body = resp.json()
        dist_m = body["features"][0]["properties"]["segments"][0]["distance"]
        dist_km = round(dist_m / 1000.0, 3)
        entry = {
            "from": city_from,
            "to": city_to,
            "distance_km": dist_km,
            "profile": "driving-car",
        }
        history.append(entry)
        return entry, 200
    except requests.RequestException:
        return {"error": "Failed to contact OpenRouteService"}, 502
    except (KeyError, IndexError, TypeError, ValueError):
        return {"error": "Unexpected response from OpenRouteService"}, 502


@app.get("/history")
def get_history():
    return {"history": history}, 200

if __name__ == "__main__":
    app.run(debug=True)