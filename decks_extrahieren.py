import ast
from pathlib import Path

import pandas as pd


# -----------------------------
# Pfade
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "all_players_clean.csv"


# -----------------------------
# Hilfsfunktion: String → Liste
# -----------------------------
def parse_players(field):
    if pd.isna(field):
        return []
    try:
        return ast.literal_eval(field)
    except Exception:
        return []


# -----------------------------
# 1. Battle-Daten laden (CSV)
# -----------------------------
def load_battles():
    df = pd.read_csv(DATA_PATH)

    print("Anzahl Battles:", len(df))
    print("Spalten:", list(df.columns))

    # Jede Zeile = ein Battle
    battles = df.to_dict(orient="records")
    return battles


# -----------------------------
# 2. Decks extrahieren
# -----------------------------
def extract_decks(all_battles):
    decks = []

    for battle in all_battles:
        team = parse_players(battle.get("team"))
        opponent = parse_players(battle.get("opponent"))

        # Team-Deck
        if team and "cards" in team[0]:
            team_cards = [c["name"] for c in team[0]["cards"]]
            if len(team_cards) == 8:
                decks.append(team_cards)

        # Opponent-Deck
        if opponent and "cards" in opponent[0]:
            opp_cards = [c["name"] for c in opponent[0]["cards"]]
            if len(opp_cards) == 8:
                decks.append(opp_cards)

    print("Extrahierte Decks:", len(decks))
    print("Beispiel-Deck:", decks[0] if decks else "keins")
    return decks


# -----------------------------
# 3. Decks als CSV speichern
# -----------------------------
def decks_to_csv(decks, output_path):
    rows = []

    for i, deck in enumerate(decks):
        row = {"deck_id": i}
        for j, card in enumerate(deck):
            row[f"card_{j+1}"] = card
        rows.append(row)

    df = pd.DataFrame(rows)
    df.to_csv(output_path, index=False, encoding="utf-8")

    print(f"CSV gespeichert unter: {output_path}")
    print("Shape:", df.shape)
    print(df.head())


if __name__ == "__main__":
    # 1) Battles laden
    battles = load_battles()

    # 2) Decks extrahieren
    decks = extract_decks(battles)

    # 3) Als CSV speichern
    output_path = BASE_DIR / "data" / "decks.csv"
    decks_to_csv(decks, output_path)
