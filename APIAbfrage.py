import requests
import json

# === Deine Daten hier eintragen ===
API_KEY = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImI4ZjIwMDc4LWNiMmYtNDU3Mi04YTlhLTdjOTYxYmE0YTg5MiIsImlhdCI6MTc2NTExOTUxMywic3ViIjoiZGV2ZWxvcGVyL2FlNjI2OGI1LWQ0MjgtOWE3OS1iOTdmLTUwZTM3YjAzYjEwZCIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyIxOTUuMTQuMjIxLjM5Il0sInR5cGUiOiJjbGllbnQifV19.rADbKN7rchGHAopk2ExBzShyYr_Lizzx3CcRDMB1zxl9ZxVCJqOiFVE4euRg8PnrYUwB9UReHQtIMgKhDJvDJQ"
PLAYER_TAG = "%23YPGPP92Q"                  # dein Clash-Royale-Spieler-Tag (das # wird durch %23 ersetzt)
# Moritz = %23YPGPP92Q
# Fabian = %23YYLQU929C
# Armin =  %23UG89PG9CU
# Joann =  %23VLP2J9VGL
# === API-Abfrage vorbereiten ===
url = f"https://api.clashroyale.com/v1/players/{PLAYER_TAG}/battlelog"
headers = {"Authorization": f"Bearer {API_KEY}"}

# === Anfrage senden ===
response = requests.get(url, headers=headers)

print("Status:", response.status_code)

if response.status_code == 200:
    data = response.json()

    # JSON-Datei speichern
    with open("C:\\TH Köln Data and Information Science\\3. Semster\\CrProjekt\\Daten\\battlelog_Moritz07.12.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✅ Erfolgreich {len(data)} Kämpfe gespeichert in 'battlelog.json'!")
else:
    print("⚠️ Fehler:", response.text)
