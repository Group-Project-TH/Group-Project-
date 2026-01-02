import os
import json
import pandas as pd
from datetime import datetime

# =========================
# 0) Pfade (DEIN Pfad)
# =========================
JSON_PATH = r"C:\Users\Marti\Desktop\Datenmodellierung_eigene_Datebn\all_players_battles_besser\all_players_battles_besser.json"
BASE_DIR = os.path.dirname(JSON_PATH)

OUTPUT_CSV  = os.path.join(BASE_DIR, "all_players_clean.csv")
OUTPUT_JSON = os.path.join(BASE_DIR, "all_players_clean.json")

# =========================
# 1) Einstellungen (Dedupe + Filter)
# =========================
# Dubletten-Definition (angepasst für alle Spieler: player_tag statt player)
subset_cols = ["battleTime", "player_tag", "type", "gameMode.id", "arena.id", "leagueNumber"]

# Unerwünschte type / gameMode.name (case-insensitive)
exclude_types = {"boatbattle", "riverraceduel"}
exclude_gamemodes = {
    "challenge_allcards_eventdeck_noset",
    "clanwar_boatbattle",
    "draftmode",
    "draft_competitive",
    "heist_friendly",
    "pickmode",
    "touchdown_draft",
}

# =========================
# 2) JSON laden
# =========================
with open(JSON_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

# =========================
# 3) Struktur: dict -> playerKey -> {"tag":..., "battles":[...]}
# =========================
dfs = []

if isinstance(data, dict):
    for player_key, player_obj in data.items():
        if not isinstance(player_obj, dict):
            continue

        battles = player_obj.get("battles", [])
        if not isinstance(battles, list) or len(battles) == 0:
            continue

        df = pd.json_normalize(battles)
        df["source_file"] = JSON_PATH
        df["player_tag"] = player_obj.get("tag", player_key)  # robust
        dfs.append(df)

elif isinstance(data, list):
    # Fallback: falls top-level doch Liste ist
    df = pd.json_normalize(data)
    df["source_file"] = JSON_PATH
    df["player_tag"] = "Unknown"
    dfs.append(df)

else:
    raise ValueError(f"Unerwartiger JSON-Typ: {type(data)}")

if not dfs:
    raise ValueError("Keine Battles gefunden. Bitte prüfe die JSON-Struktur.")

all_datalog = pd.concat(dfs, ignore_index=True)
print("Zeilen geladen:", len(all_datalog))
print("Spalten:", list(all_datalog.columns))

# =========================
# 4) Dubletten entfernen
# =========================
before = len(all_datalog)
cleaned = all_datalog.drop_duplicates(subset=subset_cols, keep="first").copy()
after = len(cleaned)

print("\nDedupe:")
print("Zeilen vor:", before)
print("Zeilen nach:", after)
print("Entfernte Dubletten:", before - after)

# =========================
# 5) Filter: type / gameMode.name entfernen
# =========================
# robust gegen NaN + SettingWithCopyWarning vermeiden
cleaned.loc[:, "type"] = cleaned["type"].astype("string").str.lower()
cleaned.loc[:, "gameMode.name"] = cleaned["gameMode.name"].astype("string").str.lower()

before_filter = len(cleaned)
cleaned = cleaned[
    (~cleaned["type"].isin(exclude_types)) &
    (~cleaned["gameMode.name"].isin(exclude_gamemodes))
].copy()

after_filter = len(cleaned)

print("\nType/GameMode Filter:")
print("Zeilen vor Filter:", before_filter)
print("Zeilen nach Filter:", after_filter)
print("Entfernte Battles:", before_filter - after_filter)

# =========================
# 6) Zusätzliche Bereinigung
# =========================
# battleTime sauber parsen (Format wie 20231204T154623.000Z)
if "battleTime" in cleaned.columns:
    cleaned.loc[:, "battleTime"] = pd.to_datetime(
        cleaned["battleTime"],
        format="%Y%m%dT%H%M%S.%fZ",
        errors="coerce",
        utc=True
    )

# numerische Spalten casten (nur wenn vorhanden)
int_cols = ["leagueNumber", "arena.id", "gameMode.id",
            "newTowersDestroyed", "prevTowersDestroyed", "remainingTowers"]
for col in int_cols:
    if col in cleaned.columns:
        cleaned.loc[:, col] = pd.to_numeric(cleaned[col], errors="coerce")

# Plausibilität Tower-Spalten (0..3)
for col in ["newTowersDestroyed", "prevTowersDestroyed", "remainingTowers"]:
    if col in cleaned.columns:
        mask_valid = cleaned[col].isna() | ((cleaned[col] >= 0) & (cleaned[col] <= 3))
        cleaned = cleaned[mask_valid].copy()

# battle_id erzeugen (praktisch)
cleaned.loc[:, "battle_id"] = cleaned["player_tag"].astype(str) + "_" + cleaned["battleTime"].astype(str)

# sortieren
sort_cols = [c for c in ["player_tag", "battleTime"] if c in cleaned.columns]
if sort_cols:
    cleaned = cleaned.sort_values(sort_cols)

# =========================
# 7) Reports / Checks
# =========================
print("\nMissing Values (Top 15):")
print(cleaned.isna().sum().sort_values(ascending=False).head(15))

remaining_dupes = cleaned.duplicated(subset=subset_cols).sum()
print("\nVerbleibende Dubletten:", remaining_dupes)

# =========================
# 8) Speichern (Permission-safe)
# =========================
def safe_save_csv(df, path):
    try:
        df.to_csv(path, index=False)
        print("CSV gespeichert:", path)
        return path
    except PermissionError:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        alt = path.replace(".csv", f"_{ts}.csv")
        df.to_csv(alt, index=False)
        print("CSV war gesperrt (z.B. Excel offen). Gespeichert:", alt)
        return alt

def safe_save_json(df, path):
    try:
        df.to_json(path, orient="records", indent=2, force_ascii=False)
        print("JSON gespeichert:", path)
        return path
    except PermissionError:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        alt = path.replace(".json", f"_{ts}.json")
        df.to_json(alt, orient="records", indent=2, force_ascii=False)
        print("JSON war gesperrt. Gespeichert:", alt)
        return alt

safe_save_csv(cleaned, OUTPUT_CSV)
safe_save_json(cleaned, OUTPUT_JSON)

print("\nFertig ✅")