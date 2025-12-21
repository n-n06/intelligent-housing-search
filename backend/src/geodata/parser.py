import os
import sys
import re

from bs4 import BeautifulSoup

sys.path.insert(
    0, 
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
)


def parse(html: str):
    """
    Parses and HTML page into a JSON array of listings
    """

    soup = BeautifulSoup(html, "html.parser")

    cards = soup.select("div.a-card")
    results = []

    for card in cards:
        # id
        external_id = card.get("data-id")

        # title 
        title_text = card.select_one(".a-card__title").get_text(strip=True)

        # extract attributes
        rooms = re.search(r"(\d+)-комнатная", title_text)
        area = re.search(r"([\d\.]+)\s*м²", title_text)
        floor = re.search(r"(\d+/\d+)\s*этаж", title_text)
            
        if rooms and rooms.group(0)[0].isdigit():
            rooms = int(rooms.group(0)[0])
        else:
            rooms = 1

        # price!!
        price_raw = card.select_one(".a-card__price").get_text(" ", strip=True)
        price_digits = int(re.sub(r"[^\d]", "", price_raw))

        # address
        subtitle = card.select_one(".a-card__subtitle").get_text(" ", strip=True)

        parts = [p.strip() for p in subtitle.split(",")]

        district = parts[0] if len(parts) > 0 else None

        # street and house number (before " — …")
        # street_part = subtitle.split("—")[0]
        # street = street_part.split(",")[-1].strip()

        street = parts[1:][0] if len(parts) > 0 else None

        # nearby objec

        # building information
        preview = card.select_one(".a-card__text-preview").get_text(" ", strip=True)

        complex_name = None
        if "жил. комплекс" in preview:
            m = re.search(r"жил\. комплекс\s+([A-Za-zА-Яа-я0-9\-«»]+)", preview)
            if m:
                complex_name = m.group(1)

        year = re.search(r"(\d{4})\s*г\.п\.", preview)

        # photo of appartment
        photo = card.select_one(".a-image__img")["src"]

        # description
        description = card.select_one(".a-card__text-preview").get_text(strip=True)

        # final json
        data = {
            "external_id": external_id,
            "title": title_text,
            "room_count": rooms,
            "area": float(area.group(1)) if area else None,
            "floor": floor.group(1) if floor else None,
            "description": description,
            "price": price_digits,
            "location": {
                "region_name": district,
                "address": street,
            },
            "complex": complex_name,
            "year_built": int(year.group(1)) if year else None,
            "photo": photo
        }

        results.append(data)

    return results


# async def main():
#     results = await parse(page=2)
#     result = results[1]
#
#     address = result["location"]["street"]
#     weather_data = await get_environment_data(address)
#
#     coord = weather_data["coordinates"]
#     lat = coord["lat"]
#     lon = coord["lon"]
#
#     nearby = await get_nearby(lat, lon)
#
#
#     return {
#         "listing": result,
#         "weather": weather_data,
#         "nearby": nearby,
#     }
#
#
#
# if __name__ == "__main__":
#     asyncio.run(main())
