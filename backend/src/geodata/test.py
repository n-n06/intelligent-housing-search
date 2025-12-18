from src.geodata.city_infra import get_nearby
from src.geodata.weather import get_environment_data


async def test_get_info(address: str):

    weather_data = await get_environment_data(address)

    coord = weather_data["coordinates"]
    lat = coord["lat"]
    lon = coord["lon"]

    nearby = await get_nearby(lat, lon)


    return {
        "weather": weather_data,
        "nearby": nearby,
    }
