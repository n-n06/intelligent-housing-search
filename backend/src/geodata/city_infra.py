import asyncio
import aiohttp

from src.geodata import state
from src.geodata.utils import (
    get_overpass_url,
    EDU_AMENITIES,
    FOOD_AMENITIES,
    FOOD_SHOPS,
    HEALTH_AMENITIES,
    TRANSPORT_AMENITIES
)

sem_overpass = asyncio.Semaphore(3)


async def overpass_query(query: str) -> dict:
    async with sem_overpass:
        async with state.session.post(
            url=get_overpass_url(),
            data={"data": query},
            timeout=aiohttp.ClientTimeout(total=30)
        ) as resp:
            resp.raise_for_status()
            return await resp.json()


def build_amenity_query(
    amenities: list[str],
    lat: float,
    lon: float,
    radius: int
) -> str:
    """
    Build a safe Overpass QL query for amenity search
    around a point.
    """
    regex = "|".join(amenities)

    return f"""
    [out:json][timeout:45];
    (
      node["amenity"~"^({regex})$"](around:{radius},{lat},{lon});
      way["amenity"~"^({regex})$"](around:{radius},{lat},{lon});
      relation["amenity"~"^({regex})$"](around:{radius},{lat},{lon});
    );
    out center;
    """


async def get_nearby_pois(
    lat: float,
    lon: float,
    amenities: list[str],
    radius: int = 1000
) -> list[dict]:

    query = build_amenity_query(amenities, lat, lon, radius)
    data = await overpass_query(query)

    pois: list[dict] = []

    for el in data.get("elements", []):
        tags = el.get("tags", {})

        name = tags.get("name")
        amenity = tags.get("amenity")

        if not name or not amenity:
            continue

        # Handle node vs way/relation
        el_lat = el.get("lat") or el.get("center", {}).get("lat")
        el_lon = el.get("lon") or el.get("center", {}).get("lon")

        if el_lat is None or el_lon is None:
            continue

        pois.append({
            "id": el["id"],
            "type": amenity,
            "name": name,
            "lat": el_lat,
            "lon": el_lon
        })

    return pois


async def get_nearby_edu(lat: float, lon: float, radius: int = 2000):
    return await get_nearby_pois(lat, lon, EDU_AMENITIES, radius)


def build_food_query(
    lat: float,
    lon: float,
    radius: int
) -> str:

    amenity_regex = "|".join(FOOD_AMENITIES)
    shop_regex = "|".join(FOOD_SHOPS)

    return f"""
    [out:json][timeout:25];
    (
      node["amenity"~"^({amenity_regex})$"](around:{radius},{lat},{lon});
      way["amenity"~"^({amenity_regex})$"](around:{radius},{lat},{lon});
      relation["amenity"~"^({amenity_regex})$"](around:{radius},{lat},{lon});

      node["shop"~"^({shop_regex})$"](around:{radius},{lat},{lon});
      way["shop"~"^({shop_regex})$"](around:{radius},{lat},{lon});
      relation["shop"~"^({shop_regex})$"](around:{radius},{lat},{lon});
    );
    out center;
    """

async def get_nearby_food(lat: float, lon: float, radius: int = 1500):
    query = build_food_query(lat, lon, radius)
    data = await overpass_query(query)

    pois = []

    for el in data.get("elements", []):
        tags = el.get("tags", {})
        name = tags.get("name")

        if not name:
            continue

        el_lat = el.get("lat") or el.get("center", {}).get("lat")
        el_lon = el.get("lon") or el.get("center", {}).get("lon")

        if el_lat is None or el_lon is None:
            continue

        poi_type = tags.get("amenity") or tags.get("shop")

        pois.append({
            "id": el["id"],
            "type": poi_type,
            "category": "amenity" if "amenity" in tags else "shop",
            "name": name,
            "lat": el_lat,
            "lon": el_lon
        })

    return pois

async def get_nearby_health(lat: float, lon: float, radius: int = 1500):
    return await get_nearby_pois(lat, lon, HEALTH_AMENITIES, radius)

async def get_nearby_transport(lat: float, lon: float, radius: int = 1000):
    return await get_nearby_pois(lat, lon, TRANSPORT_AMENITIES, radius)


async def get_nearby(lat: float, lon: float) -> dict:
    edu_task = asyncio.create_task(get_nearby_edu(lat, lon))
    food_task = asyncio.create_task(get_nearby_food(lat, lon))
    health_task = asyncio.create_task(get_nearby_health(lat, lon))
    transport_task = asyncio.create_task(get_nearby_transport(lat, lon))

    edu, food, health, transport = await asyncio.gather(
        edu_task,
        food_task,
        health_task,
        transport_task
    )

    return {
        "education": edu,
        "food": food,
        "health": health,
        "transport": transport
    }
