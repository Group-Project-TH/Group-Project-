import json
import pandas as pd
import glob
import os
import re

# 1. Alle battlelog-Dateien finden
paths = glob.glob(r"data/battlelog*.json")
print("Gefundene Dateien:", paths)

dfs = []

# 2. Dateien einlesen + Player automatisch erkennen
for p in paths:
    print("Lese Datei:", p)
    with open(p, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Falls data eine Liste ist
    if isinstance(data, list):
        records = data
    # Falls data ein Dict mit Key "battles" ist
    elif isinstance(data, dict) and "battles" in data:
        records = data["battles"]
    else:
        print("Unerwartige Struktur in:", p, "Typ:", type(data))
        continue

    # In DataFrame umwandeln
    df = pd.json_normalize(records)
    df["source_file"] = p

    # Spielername aus Dateiname extrahieren
    filename = os.path.basename(p)                      # "battlelog_Name04.12.json"
    middle = filename.replace("battlelog_", "")         # "Name04.12.json"
    middle = middle.split(".")[0]                       # "Name04"
    player_name = re.match(r"[A-Za-z]+", middle).group(0)  # "Name"

    df["player"] = player_name
    dfs.append(df)

# 3. Alle DataFrames zusammenführen
if not dfs:
    raise ValueError("Keine DataFrames erzeugt – bitte JSON-Struktur oder Pfad prüfen.")

all_datalog = pd.concat(dfs, ignore_index=True)

print("Zeilen vor Dubletten-Entfernung:", len(all_datalog))

# 4. Dubletten entfernen
subset_cols = ["battleTime", "player", "type", "gameMode.id", "arena.id", "leagueNumber"]

before = len(all_datalog)
cleaned = all_datalog.drop_duplicates(subset=subset_cols, keep="first")
after = len(cleaned)

print("Zeilen vorher:", before)
print("Zeilen nachher:", after)
print("Entfernte Dubletten:", before - after)

# 5. Speichern
output_csv = r"data/datalog_ohne_dubletten.csv"
output_json = r"data/datalog_ohne_dubletten.json"

cleaned.to_csv(output_csv, index=False)
cleaned.to_json(output_json, orient="records", indent=2, force_ascii=False)

print("CSV gespeichert unter:", output_csv)
print("JSON gespeichert unter:", output_json)