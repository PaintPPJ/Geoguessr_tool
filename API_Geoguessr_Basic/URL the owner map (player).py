import requests
import json
from urllib.parse import urlparse


NCFA = "" #ต้องใส่


session = requests.Session()

session.cookies.set(
    "_ncfa",
    NCFA,
    domain="www.geoguessr.com"
)

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
}


def get_creator_from_map_url(map_url):

    # =====================================
    # Extract Map ID
    # =====================================

    path = urlparse(map_url).path

    parts = path.strip("/").split("/")

    try:
        index = parts.index("maps")
        map_id = parts[index + 1]

    except (ValueError, IndexError):
        print("❌ ไม่พบ Map ID")
        return None


    print("Map ID:", map_id)


    # =====================================
    # Get Map
    # =====================================

    url = f"https://www.geoguessr.com/api/maps/{map_id}"

    response = session.get(
        url,
        headers=headers
    )

    print("URL:", response.url)
    print("Status:", response.status_code)


    if not response.ok:

        print("❌ API Error")
        print(response.text[:2000])

        return None


    # =====================================
    # JSON
    # =====================================

    try:

        data = response.json()

    except requests.exceptions.JSONDecodeError:

        print("❌ Response ไม่ใช่ JSON")
        print(response.text[:2000])

        return None


    # =====================================
    # Creator
    # =====================================

    creator = data.get("creator")

    if not creator:

        print("❌ ไม่พบ creator")

        return None


    return {
        "map_id": data.get("id"),
        "map_name": data.get("name"),

        "creator_name": creator.get("nick"),
        "creator_id": creator.get("id"),
        "creator_url": creator.get("url"),

        "country": creator.get("countryCode"),
    }


# ==========================================
# MAIN
# ==========================================

MAP_URL = input("Map URL: ").strip()

result = get_creator_from_map_url(MAP_URL)


if result:

    print()
    print("==============================")
    print("MAP CREATOR")
    print("==============================")

    print("Map Name :", result["map_name"])
    print("Map ID   :", result["map_id"])

    print()
    print("Username :", result["creator_name"])
    print("Player ID:", result["creator_id"])
    print("Profile  :", result["creator_url"])
    print("Country  :", result["country"])