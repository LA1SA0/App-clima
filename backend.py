from flask import Flask, request, jsonify
from api.open_meteo import get_weather_data, get_weather_forecast_data
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/api/weather", methods=["GET"])
def weather():
    city = request.args.get("city")
    if not city:
        return jsonify({"error": "Parâmetro 'city' obrigatório."}), 400
    temp = get_weather_data(city)
    forecast = get_weather_forecast_data(city)
    if temp is None or forecast is None:
        return jsonify({"error": "Não foi possível obter os dados do clima."}), 404
    # Dados do dia atual
    wcode = forecast['weathercode'][0]
    desc = "-"
    weather_codes = {
        0: "Ensolarado",
        1: "Principalmente ensolarado",
        2: "Parcialmente nublado",
        3: "Nublado",
        45: "Névoa",
        48: "Névoa gelada",
        51: "Garoa leve",
        53: "Garoa moderada",
        55: "Garoa densa",
        61: "Chuva leve",
        63: "Chuva moderada",
        65: "Chuva forte",
        80: "Aguaceiros leves",
        81: "Aguaceiros moderados",
        82: "Aguaceiros violentos",
        95: "Trovoada",
        96: "Trovoada com granizo leve",
        99: "Trovoada com granizo forte"
    }
    desc = weather_codes.get(wcode, "-")
    vento = forecast['windspeed_10m_max'][0]
    return jsonify({
        "city": city,
        "temperature": temp,
        "description": desc,
        "wind": vento,
        "forecast": forecast
    })

if __name__ == "__main__":
    app.run(debug=True)
