import asyncio

from src.cache import cache, cache_key
from src.config import settings
from src.geodata.utils import fetch_json


async def _geocode_yandex(address: str) -> dict:
    key = cache_key("yandex", address)
    cached = await cache.get(key)
    if cached:
        return cached

    url = "https://geocode-maps.yandex.ru/v1/"
    params = {
        "apikey": settings.YANDEX_API_KEY,
        "format": "json",
        "geocode": address,
        "results": 1,
        "lang": "ru_RU",
    }

    data = await fetch_json(url, params)

    members = data["response"]["GeoObjectCollection"].get("featureMember", [])
    if not members:
        raise ValueError(f"Address not found: {address}")

    geo = members[0]["GeoObject"]
    lon_str, lat_str = geo["Point"]["pos"].split()

    result = {
        "lat": float(lat_str),
        "lon": float(lon_str),
        "formatted": geo["metaDataProperty"]["GeocoderMetaData"]["text"],
    }

    await cache.set(key, result)
    return result


async def _get_weather(lat: float, lon: float) -> dict:
    key = cache_key("weather", f"{lat}:{lon}")
    cached = await cache.get(key)
    if cached:
        return cached

    url = "https://api.openweathermap.org/data/3.0/onecall"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": settings.OPENWEATHER_API_KEY,
        "units": "metric",
    }

    data = await fetch_json(url, params)
    result = {
        "temperature": data.get("current", {}).get("temp"),
        "humidity": data.get("current", {}).get("humidity"),
        "wind_speed": data.get("current", {}).get("wind_speed"),
        "uvi": data.get("current", {}).get("uvi"),
    }

    await cache.set(key, result)
    return result


async def _get_air_quality(lat: float, lon: float) -> dict:
    key = cache_key("aqi", f"{lat}:{lon}")
    cached = await cache.get(key)
    if cached:
        return cached

    url = "https://api.openweathermap.org/data/2.5/air_pollution"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": settings.OPENWEATHER_API_KEY,
    }

    data = await fetch_json(url, params)

    if not data.get("list"):
        result = {}
    else:
        comp = data["list"][0]
        result = {
            "aqi": comp["main"]["aqi"],
            "components": comp["components"],
        }

    await cache.set(key, result)
    return result


async def _get_environment_data(address: str) -> dict:
    coords = await _geocode_yandex(address)
    lat, lon = coords["lat"], coords["lon"]

    weather_task = asyncio.create_task(_get_weather(lat, lon))
    aqi_task = asyncio.create_task(_get_air_quality(lat, lon))

    weather, aqi = await asyncio.gather(weather_task, aqi_task)

    return {
        "address": coords.get("formatted", address),
        "coordinates": {"lat": lat, "lon": lon},
        "weather": weather,
        "air_quality": aqi,
    }


async def get_environment_data(adresss: str):
    return await _get_environment_data(adresss)


