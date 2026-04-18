import httpx
from datetime import datetime
from typing import Optional

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"
GEOCODING_URL  = "https://geocoding-api.open-meteo.com/v1/search"

WEATHER_CODES: dict[int, tuple[str, str]] = {
    0:  ("Céu limpo",            "clear"),
    1:  ("Principalmente limpo", "mostly-clear"),
    2:  ("Parcialmente nublado", "partly-cloudy"),
    3:  ("Nublado",              "cloudy"),
    45: ("Neblina",              "fog"),
    48: ("Neblina com gelo",     "fog"),
    51: ("Garoa leve",           "drizzle"),
    53: ("Garoa moderada",       "drizzle"),
    55: ("Garoa intensa",        "drizzle"),
    61: ("Chuva leve",           "rain"),
    63: ("Chuva moderada",       "rain"),
    65: ("Chuva forte",          "heavy-rain"),
    71: ("Neve leve",            "snow"),
    73: ("Neve moderada",        "snow"),
    75: ("Neve intensa",         "heavy-snow"),
    80: ("Pancadas leves",       "showers"),
    81: ("Pancadas moderadas",   "showers"),
    82: ("Pancadas fortes",      "heavy-showers"),
    95: ("Tempestade",           "storm"),
    99: ("Tempestade c/ granizo","storm"),
}

DAYS_PT = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]


def get_weather_info(code: int) -> tuple[str, str]:
    return WEATHER_CODES.get(code, ("Condição desconhecida", "unknown"))


async def geocode(city: str) -> Optional[dict]:
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(GEOCODING_URL, params={
            "name": city, "count": 5, "language": "pt", "format": "json"
        })
        data = r.json()
        results = data.get("results", [])
        if not results:
            return None
        top = results[0]
        return {
            "lat":     top["latitude"],
            "lon":     top["longitude"],
            "city":    top["name"],
            "country": top.get("country", ""),
            "admin":   top.get("admin1", ""),
        }


async def fetch_weather(lat: float, lon: float) -> dict:
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(OPEN_METEO_URL, params={
            "latitude":  lat,
            "longitude": lon,
            "current":   "temperature_2m,relative_humidity_2m,wind_speed_10m,"
                         "weather_code,apparent_temperature,precipitation,surface_pressure,"
                         "visibility,uv_index",
            "daily":     "temperature_2m_max,temperature_2m_min,weather_code,"
                         "precipitation_sum,wind_speed_10m_max,uv_index_max,"
                         "sunrise,sunset",
            "hourly":    "precipitation,temperature_2m",
            "timezone":  "auto",
            "forecast_days": 7,
        })
        return r.json()


async def fetch_rain_regions(lat: float, lon: float) -> list[dict]:
    """
    Fetch nearby region weather data to show rainfall on map.
    Creates a grid of points around the searched location.
    """
    offsets = [
        (-2.0, -2.0), (-2.0, 0), (-2.0, 2.0),
        ( 0.0, -2.0), ( 0.0, 0), ( 0.0, 2.0),
        ( 2.0, -2.0), ( 2.0, 0), ( 2.0, 2.0),
    ]
    regions = []
    async with httpx.AsyncClient(timeout=15) as client:
        for dlat, dlon in offsets:
            rlat, rlon = lat + dlat, lon + dlon
            try:
                r = await client.get(OPEN_METEO_URL, params={
                    "latitude":  rlat,
                    "longitude": rlon,
                    "current":   "precipitation,weather_code,temperature_2m",
                    "timezone":  "auto",
                })
                d = r.json()
                cur = d.get("current", {})
                code = cur.get("weather_code", 0)
                _, condition = get_weather_info(code)
                regions.append({
                    "lat":       round(rlat, 4),
                    "lon":       round(rlon, 4),
                    "precip":    round(cur.get("precipitation", 0), 1),
                    "temp":      round(cur.get("temperature_2m", 0)),
                    "condition": condition,
                    "code":      code,
                })
            except Exception:
                pass
    return regions


def build_context(geo: dict, raw: dict, regions: list[dict]) -> dict:
    cur   = raw["current"]
    daily = raw["daily"]
    hourly = raw.get("hourly", {})

    desc, cond = get_weather_info(cur["weather_code"])

    forecast = []
    for i in range(7):
        date_obj = datetime.strptime(daily["time"][i], "%Y-%m-%d")
        d, c = get_weather_info(daily["weather_code"][i])
        forecast.append({
            "day":    DAYS_PT[date_obj.weekday()],
            "date":   date_obj.strftime("%d/%m"),
            "max":    round(daily["temperature_2m_max"][i]),
            "min":    round(daily["temperature_2m_min"][i]),
            "desc":   d,
            "cond":   c,
            "precip": round(daily["precipitation_sum"][i], 1),
            "wind":   round(daily["wind_speed_10m_max"][i]),
            "uv":     round(daily.get("uv_index_max", [0]*7)[i], 1),
            "sunrise": daily.get("sunrise", [""] * 7)[i][-5:] if daily.get("sunrise") else "",
            "sunset":  daily.get("sunset",  [""] * 7)[i][-5:] if daily.get("sunset")  else "",
        })

    # hourly precip for next 24h
    hourly_precip = []
    if hourly.get("time"):
        now_hour = datetime.now().hour
        times  = hourly["time"][:24]
        precips = hourly.get("precipitation", [0]*24)[:24]
        temps   = hourly.get("temperature_2m", [0]*24)[:24]
        for t, p, tmp in zip(times, precips, temps):
            hour = t[-5:]
            hourly_precip.append({"hour": hour, "precip": round(p, 1), "temp": round(tmp)})

    return {
        "city":        geo["city"],
        "country":     geo["country"],
        "admin":       geo["admin"],
        "lat":         geo["lat"],
        "lon":         geo["lon"],
        "temp":        round(cur["temperature_2m"]),
        "feels_like":  round(cur["apparent_temperature"]),
        "humidity":    cur["relative_humidity_2m"],
        "wind":        round(cur["wind_speed_10m"]),
        "precip":      round(cur.get("precipitation", 0), 1),
        "pressure":    round(cur.get("surface_pressure", 0)),
        "uv":          round(cur.get("uv_index", 0), 1),
        "visibility":  round(cur.get("visibility", 0) / 1000, 1),
        "desc":        desc,
        "cond":        cond,
        "forecast":    forecast,
        "hourly":      hourly_precip,
        "regions":     regions,
    }
