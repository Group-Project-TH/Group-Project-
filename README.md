# Branch: ProDaten (Top-Spieler-Daten)

## Zweck
Dieser Branch enthält die **Spieldaten von 100 Top-Spielern aus Clash Royale**.
Die Daten bilden die Grundlage für den Vergleich zwischen **Top-Spieler-Decks**
und **Casual-Spielern** im Hauptprojekt.

---

## Datenquelle
- Öffentliche Clash-Royale-APIs  über https://developer.clashroyale.com/#/
- Auswahl von 100 Top-Spielern von https://royaleapi.com/players/leaderboard deren Player Tags durch clashroyal.py gescraped und in 100top_player_ids.json gespeichert
- Download der vollständigen Battlelogs dieser Spieler durch einfügen der Player Tags in ABIAbfragenPro.py
- Die Volständige Datei heißt all_player_battle_besser.json als zip Datei hochgeladen 


---

## Verarbeitungsschritte
- Mit Datei ProData_cleaning.py werden die Daten bereinigt und als all_players_clean.csv gespeichert
- Durch auslesen der all_players_clean.csv mit werden die einezelnen Decks in extrahiert und in decks.csv gespeichert
- Mit tsne_map.py wurde die tsne Map.png erstellt
---

## Ziel
Bereitstellung eines **sauberen, konsistenten Datensatzes** von Top-Spielern,
der in visual Branche für:
- Karten- und Deck-Analysen
- Clusterbildung
- Performance-Vergleiche  
verwendet wird.


