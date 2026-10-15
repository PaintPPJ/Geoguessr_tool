
import csv
import json

INPUT_CSV = ".csv"
OUTPUT_JSON = ".json"

locations = []

with open(INPUT_CSV, "r", encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)

    for i, row in enumerate(reader, start=1):
        try:
            lat = float(row["lat"])
            lng = float(row["lng"])
        except (ValueError, KeyError, TypeError):
            continue

        locations.append({
            "lat": lat,
            "lng": lng,
            "heading": 0,
            "pitch": 0,
            "zoom": 0,
            "panoId": None,
            "countryCode": "TH",
            "stateCode": None,
            "extra": {}
        })

with open(OUTPUT_JSON, "w", encoding="utf-8") as file:
    json.dump(locations, file, ensure_ascii=False, indent=2)

print(f"สร้าง JSON สำเร็จ {len(locations)} จุด")
print(f"ไฟล์: {OUTPUT_JSON}")
