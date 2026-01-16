# Branch: ProDaten (Top-Spieler-Daten)

## Zweck
Dieser Branch enthält die **Spieldaten von 100 Top-Spielern aus Clash Royale**.
Die Daten bilden die Grundlage für den Vergleich zwischen **Top-Spieler-Decks**
und **Casual-Spielern** im Hauptprojekt.

---

## Datenquelle
- Öffentliche Clash-Royale-APIs
- Auswahl von 100 Top-Spielern (z. B. aus globalen Ranglisten)
- Download der vollständigen Battlelogs dieser Spieler

---

## Inhalt
- Rohdaten der Battlelogs (JSON / ZIP)
- Skripte zur API-Abfrage
- Skripte zur Datenbereinigung (Cleaning)
- Bereinigte CSV-Dateien für die weitere Analyse

---

## Verarbeitungsschritte
- API-Abfrage der Matches von Top-Spielern
- Zusammenführen der Battlelogs
- Entfernen von Duplikaten
- Filtern relevanter Match-Typen
- Export der bereinigten Daten in CSV-Formate

---

## Ziel
Bereitstellung eines **sauberen, konsistenten Datensatzes** von Top-Spielern,
der in späteren Branches für:
- Karten- und Deck-Analysen
- Clusterbildung
- Performance-Vergleiche  
verwendet wird.

---

## Weiterverwendung
Die hier erzeugten Datensätze werden in den Analyse- und Vergleichs-Branches
(z. B. Data Analysis, Clustering, ...) genutzt.
