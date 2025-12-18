import asyncio
import itertools

from src.geodata import state


"""
For requests
"""
sem = asyncio.Semaphore(10)
async def fetch_json(url: str, params: dict) -> dict:
    async with sem:
        async with state.session.get(url, params=params) as resp:
            resp.raise_for_status()
            return await resp.json()



"""
For Overpass
"""
OVERPASS_ENDPOINTS = [
    # "https://overpass-api.de/api/interpreter",
    "https://maps.mail.ru/osm/tools/overpass/api/interpreter",
    "https://overpass.private.coffee/api/interpreter"
]

_endpoint_iterator = itertools.cycle(OVERPASS_ENDPOINTS)

def get_overpass_url() -> str:
    return next(_endpoint_iterator)


EDU_AMENITIES = [
    "school",
    "college",
    "university",
    "kindergarten",
    "library"
]

FOOD_AMENITIES = [
    "restaurant",
    "cafe",
    "fast_food",
    "food_court",
    "bar",
    "pub",
    "ice_cream"
]

FOOD_SHOPS = [
    "supermarket",
    "convenience",
    "grocery",
    "bakery",
    "butcher",
    "greengrocer",
    "deli",
    "seafood",
    "confectionery",
    "alcohol",
    "wine",
    "beverages"
]

HEALTH_AMENITIES = [
    "clinic",
    "dentist",
    "doctors",
    "hospital",
    "pharmacy"
]

TRANSPORT_AMENITIES = [
    "parking",
    "parking_entrance",
    "fuel",
    "charging_station",
    "bus_station",
    "bicycle_parking"
]
