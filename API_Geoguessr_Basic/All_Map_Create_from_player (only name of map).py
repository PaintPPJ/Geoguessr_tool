import requests

# =========================
# CONFIG
# =========================

NCFA_COOKIE = "" #ต้องใส่

TARGET_USER_ID = ""

API_URL = "https://www.geoguessr.com/api/maps"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/140.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Cookie": f"_ncfa={NCFA_COOKIE}"
}


# =========================
# GET USER PROFILE
# =========================

def get_user_profile(user_id):

    USER_API_URL = f"https://www.geoguessr.com/api/v3/users/{user_id}"

    response = requests.get(
        USER_API_URL,
        headers=headers
    )

    print("Profile URL:", response.url)
    print("Profile Status:", response.status_code)

    if not response.ok:
        print("❌ ไม่สามารถดึงข้อมูลผู้เล่นได้")
        print(response.text[:2000])
        return None

    try:
        data = response.json()
    except requests.exceptions.JSONDecodeError:
        print("❌ Server ไม่ได้ส่ง JSON")
        print(response.text[:2000])
        return None

    return data

# =========================
# GET USER MAPS
# =========================

def get_user_maps(user_id, page=0, count=200):

    params = {
        "createdBy": user_id,
        "page": page,
        "count": count
    }

    response = requests.get(
        API_URL,
        headers=headers,
        params=params
    )

    print("URL:", response.url)
    print("Status:", response.status_code)
    print("Content-Type:", response.headers.get("Content-Type"))

    if not response.ok:
        print("❌ HTTP Error:", response.status_code)
        print(response.text[:2000])
        return []

    try:
        data = response.json()
    except requests.exceptions.JSONDecodeError:
        print("❌ Server ไม่ได้ส่ง JSON")
        print(response.text[:2000])
        return []

    # ตรวจสอบโครงสร้าง JSON
    if isinstance(data, list):
        return data

    if isinstance(data, dict):

        if "maps" in data:
            return data["maps"]

        if "results" in data:
            return data["results"]

    print("⚠️ ไม่พบ maps/results ใน JSON")
    print(data)

    return []


# =========================
# GET ALL MAPS
# =========================

all_maps = []

page = 0

while True:

    maps = get_user_maps(
        TARGET_USER_ID,
        page=page,
        count=200
    )

    print(f"Page {page}: {len(maps)} maps")

    if not maps:
        break

    all_maps.extend(maps)

    # ถ้าได้ไม่ถึง 200 แสดงว่าเป็นหน้าสุดท้าย
    if len(maps) < 200:
        break

    page += 1


# =========================
# DISPLAY
# =========================
profile = get_user_profile(TARGET_USER_ID)

if profile:
    print("\n==============================")
    print("PLAYER INFORMATION")
    print("==============================")

    print("Name:", profile.get("nick"))
    print("ID:", profile.get("id"))
    print("Country:", profile.get("countryCode"))
    print()


print("\n==============================")
print("TOTAL MAPS:", len(all_maps))
print("==============================\n")

for i, m in enumerate(all_maps, 1):

    print(f"{i}. {m.get('name')}")
