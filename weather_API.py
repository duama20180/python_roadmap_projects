import os
import requests
import redis
from flask import Flask, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv

load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
REDIS_URL = os.getenv("REDIS_URL")

r = redis.Redis.from_url(REDIS_URL, decode_responses=True)

app = Flask(__name__)

# max 5 requests per minute per IP
limiter = Limiter(app, key_func=get_remote_address, default_limits=["5 per minute"])

def get_weather_from_api(city):
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}?unitGroup=metric&key={WEATHER_API_KEY}&contentType=json"
    response = requests.get(url)
    if response.status_code != 200:
        return None, response.status_code
    return response.json(), 200

# weather endpoint
@app.route("/weather/<city>", methods=["GET"])
@limiter.limit("5 per minute")
def weather(city):
    cached_data = r.get(city)
    if cached_data:
        return jsonify({"source": "cache", "data": eval(cached_data)}), 200

    data, status = get_weather_from_api(city)
    if not data:
        return jsonify({"error": f"Could not fetch weather for {city}"}), status

    # saving data into cache for 12 hours
    r.set(city, str(data), ex=43200)

    return jsonify({"source": "api", "data": data}), 200

if __name__ == "__main__":
    app.run(debug=True)
