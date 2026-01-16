# Branch: UnsereDaten (Eigene Spieldaten)

## Zweck
Dieser Branch enthält die **eigenen Spieldaten der Projektgruppe**.
Die Daten wurden über einen längeren Zeitraum gesammelt und dienen
als Vergleichsbasis zu den Daten von Top-Spielern.

---

## Datensammlung
- Zeitraum: ca. ein Monat
- Quelle: eigene Clash-Royale-Accounts der Gruppenmitglieder
- Download der Matchhistorien über APIabfrage.py
- alle Daten im Daten ordner hochgeladen

---

## Verarbeitungsschritte
- Regelmäßige API-Abfragen der eigenen Matches
- Zusammenführung aller Spiele der Gruppenmitglieder
- Entfernen von doppelten Matches durch doubletten_entferner.py
- mit opponent_decks.py wurden alle gegnerischen uniquen Decks in opponent_decks_cleaned.csv gespeichert
- in cluster_in_unseren_daten.py wurde probiert die cluster die aus den ProDaten gewonnen wurden in opponent_decks_cleaned.csv gesucht und Ergebnisse in cluster_frequency.csv und cluster_machtes_in_opponent_decks.csv gespeichert


---



