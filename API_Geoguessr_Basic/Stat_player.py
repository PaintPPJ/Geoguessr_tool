import requests

NCFA_COOKIE = "" #Cookie token

API_URL = "https://www.geoguessr.com/api/v4/parties/v2/community/list"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/140.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Cookie": "" #ต้องใส่
}

params = {
    "page": 0,
    "count": 5
}

response = requests.post(
    API_URL,
    headers=headers,
    params=params
)

if response.ok:

    data = response.json()

    parties = data.get("parties", [])
    stats = data.get("stats", {})

    print("========== PARTY LIST ==========")
    print(f"Total: {stats.get('totalCount', 0)}")
    print(f"Ongoing: {stats.get('ongoingCount', 0)}")
    print(f"Open: {stats.get('openCount', 0)}")
    print()

    for i, party in enumerate(parties, 1):

        print(f"===== Party {i} =====")
        print("Party ID:", party.get("partyId"))
        print("Owner ID:", party.get("ownerId"))
        print("Game Mode:", party.get("gameMode"))
        print("Vibe:", party.get("vibe"))
        print("Language:", party.get("language"))
        print("Party Size:", party.get("partySize"))
        print("Game State:", party.get("gameState"))
        print(
            "Players:",
            party.get("currentNumberOfPlayers"),
            "/",
            party.get("partySize")
        )

        print("Members:")

        for member in party.get("topPartyMembers", []):

            print(
                f"  - {member.get('nick')} "
                f"(ID: {member.get('userId')}) "
                f"Team: {member.get('team')}"
            )

        print()

else:
    print("HTTP Error:", response.status_code)
    print(response.text)