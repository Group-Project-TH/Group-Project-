import json
import time
import requests
from pathlib import Path

# ⚠️ Deinen API-Key hier eintragen (NIEMALS ins Internet hochladen!)
API_KEY = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjNkMWIxZTI5LTY3YzMtNDUwMi1hMmMxLTY1MDE0NmYyOTIyYSIsImlhdCI6MTc2NTM3OTM2Niwic3ViIjoiZGV2ZWxvcGVyL2FlNjI2OGI1LWQ0MjgtOWE3OS1iOTdmLTUwZTM3YjAzYjEwZCIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyIxOTUuMTQuMjE4LjI1NSJdLCJ0eXBlIjoiY2xpZW50In1dfQ.NdCZrMS2fEsR4bBQG8Ab18owbb0B2CvRlnd0WF1d7rMUf715WwMZCnDzZCK-dlOK3LIBePl2vg397XjKV2k6ug"
BASE_URL = "https://api.clashroyale.com/v1"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}"
}

# Basis-Pfad (Ordner, in dem dieses Skript liegt)
BASE_DIR = Path(__file__).resolve().parent

# -----------------------
# 1. Player Tags einlesen
# -----------------------
PLAYER_TAGS_PATH = BASE_DIR / "100top_player_ids20251207.json"

with open(PLAYER_TAGS_PATH, "r", encoding="utf-8") as f:
    player_tags = json.load(f)

print(f"Gefundene Spieler-Tags: {len(player_tags)}")


# -----------------------
# Funktion zum Battlelog holen
# -----------------------
def get_player_battles(tag):
    """
    Holt das Battlelog für einen Spieler-Tag.
    Gibt eine Liste von Battles zurück (kann leer sein).
    """
    url = f"{BASE_URL}/players/%23{tag}/battlelog"  # %23 = "#"
    resp = requests.get(url, headers=HEADERS)

    if resp.status_code == 200:
        battles = resp.json()
        if not isinstance(battles, list):
            print(f"⚠️ Unerwartetes Format für {tag}, erwarte Liste, bekam: {type(battles)}")
            return []
        return battles

    elif resp.status_code == 429:
        print(f"⚠️ Rate Limit erreicht bei {tag}! Warte 30 Sekunden und versuche es erneut...")
        time.sleep(30)
        return get_player_battles(tag)  # Retry

    else:
        print(f"❌ Fehler {resp.status_code} für Spieler {tag}: {resp.status_code} {resp.text}")
        return []


# -----------------------
# 2. Battlelogs aller Spieler holen
# -----------------------
all_player_battles = {}  # key = tag, value = dict mit battles

for i, tag in enumerate(player_tags, start=1):
    print(f"[{i}/{len(player_tags)}] Hole Battlelog für Spieler: {tag}")

    battles = get_player_battles(tag)
    print(f"   → {len(battles)} Battles gefunden")

    # Daten strukturiert ablegen
    all_player_battles[tag] = {
        "tag": tag,
        "battleCount": len(battles),
        "battles": battles
    }

    # kleiner Delay, um das Rate Limit zu schonen
    time.sleep(0.4)

# Kurze Übersicht
total_battles = sum(player_data["battleCount"] for player_data in all_player_battles.values())
print(f"\nInsgesamt gesammelte Battles: {total_battles}")


# -----------------------
# 3. Ergebnisse in EINER Datei speichern
# -----------------------
OUTPUT_PATH = BASE_DIR / "all_players_battles.json"

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(all_player_battles, f, ensure_ascii=False, indent=2)

print(f"✅ Fertig! Battlelogs gespeichert in {OUTPUT_PATH}")

