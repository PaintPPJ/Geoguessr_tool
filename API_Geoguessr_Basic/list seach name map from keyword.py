import requests
import time

NCFA = "" #ต้องใส่

QUERY = "usa area code zone" #example Keyword
COUNT = 25

session = requests.Session()

session.cookies.set(
    "_ncfa",
    NCFA,
    domain="www.geoguessr.com"
)

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Referer": "https://www.geoguessr.com/",
}


def search_maps(query, page=0):

    url = "https://www.geoguessr.com/api/v3/search/any"

    params = {
        "page": page,
        "count": COUNT,
        "q": query
    }

    response = session.get(
        url,
        params=params,
        headers=headers,
        timeout=20
    )

    print(f"Page {page} | Status: {response.status_code}")

    if not response.ok:
        print(response.text[:1000])
        return []

    return response.json()


# ==========================================
# ดึงทุกหน้า
# ==========================================
MAX_MAPS = 1000

all_maps = []
seen_ids = set()
page = 0

while len(all_maps) < MAX_MAPS:

    data = search_maps(QUERY, page)

    if not data:
        break

    for item in data:

        # เอาเฉพาะ Map
        if item.get("type") != 1:
            continue

        map_id = item.get("id")

        if not map_id:
            continue

        # ป้องกัน Map ซ้ำ
        if map_id in seen_ids:
            continue

        seen_ids.add(map_id)

        all_maps.append({
            "name": item.get("name"),
            "url": f"https://www.geoguessr.com/maps/{map_id}"
        })

        # ครบ 1000 แล้วหยุด
        if len(all_maps) >= MAX_MAPS:
            break

    print(f"Collected: {len(all_maps)}/{MAX_MAPS}")

    # ถ้าหน้านี้มีน้อยกว่า COUNT
    # แสดงว่าไม่มีหน้าต่อไป
    if len(data) < COUNT:
        break

    page += 1

    time.sleep(0.3)


# ==========================================
# OUTPUT
# ==========================================

print("\nMAPS FOUND")
print("=" * 60)

for i, item in enumerate(all_maps, 1):

    print(f"{i}. {item['name']}")
    print(f"   {item['url']}")

print("\nTotal:", len(all_maps))