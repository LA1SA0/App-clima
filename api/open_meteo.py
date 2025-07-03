# Módulo para integração com a API Open-Meteo
import requests
import time

# Cache em memória: {cidade: (timestamp, dados)}
weather_cache = {}

def get_weather_data(city_name):
    """
    Busca a temperatura atual para a cidade informada usando a API Open-Meteo.
    Retorna a temperatura em Celsius ou None se não encontrar.
    """
    # 1. Obter latitude e longitude da cidade usando Nominatim (OpenStreetMap)
    geocode_url = f"https://nominatim.openstreetmap.org/search?format=json&q={city_name}"
    geocode_resp = requests.get(geocode_url, headers={"User-Agent": "weather-app"})
    if geocode_resp.status_code != 200 or not geocode_resp.json():
        print("Cidade não encontrada.")
        return None
    location = geocode_resp.json()[0]
    lat = location['lat']
    lon = location['lon']

    # 2. Buscar dados meteorológicos na Open-Meteo
    weather_url = (
        f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&timezone=auto"
    )
    weather_resp = requests.get(weather_url)
    if weather_resp.status_code != 200:
        print("Erro ao buscar dados do clima.")
        return None
    data = weather_resp.json()
    try:
        temp = data['current_weather']['temperature']
        return temp
    except (KeyError, TypeError):
        print("Dados de temperatura não encontrados.")
        return None

def get_weather_forecast(city_name):
    """
    Busca a previsão do tempo para os próximos 5 dias usando a API Open-Meteo.
    Exibe temperatura máxima/mínima, condição do tempo, umidade, vento e precipitação.
    """
    # 1. Obter latitude e longitude da cidade usando Nominatim
    geocode_url = f"https://nominatim.openstreetmap.org/search?format=json&q={city_name}"
    geocode_resp = requests.get(geocode_url, headers={"User-Agent": "weather-app"})
    if geocode_resp.status_code != 200 or not geocode_resp.json():
        print("Cidade não encontrada.")
        return
    location = geocode_resp.json()[0]
    lat = location['lat']
    lon = location['lon']

    # 2. Buscar previsão de 5 dias na Open-Meteo
    weather_url = (
        f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
        f"&daily=temperature_2m_max,temperature_2m_min,weathercode,precipitation_sum,windspeed_10m_max,relative_humidity_2m_max,relative_humidity_2m_min"
        f"&forecast_days=5&timezone=auto"
    )
    weather_resp = requests.get(weather_url)
    if weather_resp.status_code != 200:
        print("Erro ao buscar dados do clima.")
        return
    data = weather_resp.json()
    daily = data.get('daily', {})
    if not daily:
        print("Dados de previsão não encontrados.")
        return
    # Dicionário para traduzir weathercode
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
        56: "Garoa gelada leve",
        57: "Garoa gelada densa",
        61: "Chuva leve",
        63: "Chuva moderada",
        65: "Chuva forte",
        66: "Chuva congelante leve",
        67: "Chuva congelante forte",
        71: "Neve leve",
        73: "Neve moderada",
        75: "Neve forte",
        77: "Grãos de neve",
        80: "Aguaceiros leves",
        81: "Aguaceiros moderados",
        82: "Aguaceiros violentos",
        85: "Aguaceiros de neve leves",
        86: "Aguaceiros de neve fortes",
        95: "Trovoada",
        96: "Trovoada com granizo leve",
        99: "Trovoada com granizo forte"
    }
    # Exibir previsão formatada
    for i in range(5):
        dia = daily['time'][i]
        tmax = daily['temperature_2m_max'][i]
        tmin = daily['temperature_2m_min'][i]
        wcode = daily['weathercode'][i]
        clima = weather_codes.get(wcode, "Desconhecido")
        umidade_max = daily.get('relative_humidity_2m_max', [None]*5)[i]
        umidade_min = daily.get('relative_humidity_2m_min', [None]*5)[i]
        umidade = f"{umidade_min}% - {umidade_max}%" if umidade_min and umidade_max else "-"
        vento = daily.get('windspeed_10m_max', [None]*5)[i]
        vento_str = f"{vento} km/h" if vento is not None else "-"
        precipitacao = daily.get('precipitation_sum', [None]*5)[i]
        precipitacao_str = f"{precipitacao} mm" if precipitacao is not None else "-"
        print(f"Dia {dia}")
        print(f"Temp: {tmax}°C / {tmin}°C")
        print(f"Clima: {clima}")
        print(f"Umidade: {umidade}")
        print(f"Vento: {vento_str}")
        print(f"Precipitação: {precipitacao_str}")
        print("-"*30)

def get_weather_with_cache(city_name):
    """
    Retorna previsão do tempo da cidade usando cache em memória.
    Se os dados tiverem menos de 1 hora, retorna do cache.
    Caso contrário, busca da API, salva no cache e retorna.
    """
    now = time.time()
    cache_entry = weather_cache.get(city_name.lower())
    if cache_entry:
        timestamp, dados = cache_entry
        if now - timestamp < 3600:  # 1 hora = 3600 segundos
            print("[CACHE] Dados de previsão recentes encontrados.")
            return dados
    # Buscar da API
    print("[API] Buscando dados atualizados...")
    # Reutiliza a função get_weather_forecast, mas retorna os dados em vez de imprimir
    dados = get_weather_forecast_data(city_name)
    if dados:
        weather_cache[city_name.lower()] = (now, dados)
    return dados

def get_weather_forecast_data(city_name):
    """
    Busca a previsão do tempo para os próximos 5 dias e retorna os dados em dicionário.
    """
    geocode_url = f"https://nominatim.openstreetmap.org/search?format=json&q={city_name}"
    geocode_resp = requests.get(geocode_url, headers={"User-Agent": "weather-app"})
    if geocode_resp.status_code != 200 or not geocode_resp.json():
        print("Cidade não encontrada.")
        return None
    location = geocode_resp.json()[0]
    lat = location['lat']
    lon = location['lon']
    weather_url = (
        f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
        f"&daily=temperature_2m_max,temperature_2m_min,weathercode,precipitation_sum,windspeed_10m_max,relative_humidity_2m_max,relative_humidity_2m_min"
        f"&forecast_days=5&timezone=auto"
    )
    weather_resp = requests.get(weather_url)
    if weather_resp.status_code != 200:
        print("Erro ao buscar dados do clima.")
        return None
    data = weather_resp.json()
    daily = data.get('daily', {})
    if not daily:
        print("Dados de previsão não encontrados.")
        return None
    return daily

if __name__ == "__main__":
    cidade = input("Digite o nome da cidade: ")
    temperatura = get_weather_data(cidade)
    if temperatura is not None:
        print(f"Temperatura atual em {cidade}: {temperatura}°C")
    else:
        print("Não foi possível obter a temperatura.")
    print("\nPrevisão para os próximos 5 dias:\n")
    get_weather_forecast(cidade)
