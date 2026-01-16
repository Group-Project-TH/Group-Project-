import ast
from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE


# --------------------------------------------------
# Pfade
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "all_players_clean.csv"


# --------------------------------------------------
# Hilfsfunktion: String → Liste
# --------------------------------------------------
def parse_players(field):
    if pd.isna(field):
        return []
    try:
        return ast.literal_eval(field)
    except Exception:
        return []


# --------------------------------------------------
# 1. Battles laden
# --------------------------------------------------
def load_battles():
    df = pd.read_csv(DATA_PATH)
    print("Anzahl Battles:", len(df))
    return df.to_dict(orient="records")


# --------------------------------------------------
# 2. Decks extrahieren (nur 8-Karten-Decks)
# --------------------------------------------------
def extract_decks(all_battles):
    decks = []

    for battle in all_battles:
        team = parse_players(battle.get("team"))
        opponent = parse_players(battle.get("opponent"))

        if team and "cards" in team[0]:
            cards = [c["name"] for c in team[0]["cards"]]
            if len(cards) == 8:
                decks.append(cards)

        if opponent and "cards" in opponent[0]:
            cards = [c["name"] for c in opponent[0]["cards"]]
            if len(cards) == 8:
                decks.append(cards)

    print("Extrahierte Decks:", len(decks))
    return decks


# --------------------------------------------------
# 3. One-Hot-Encoding (Decks × Karten)
# --------------------------------------------------
def build_one_hot(decks):
    all_cards = sorted({card for deck in decks for card in deck})
    df = pd.DataFrame(0, index=range(len(decks)), columns=all_cards)

    for i, deck in enumerate(decks):
        for card in deck:
            df.at[i, card] = 1

    print("One-Hot Shape:", df.shape)
    return df


# --------------------------------------------------
# 4. t-SNE Karten-Map (Co-Occurrence)
# --------------------------------------------------
def build_card_map(df):
    cards = df.columns

    # Co-Occurrence Matrix
    co_matrix = df.T.dot(df)

    # Distanz = je seltener zusammen, desto größer
    max_val = co_matrix.values.max()
    dist_matrix = max_val - co_matrix.values

    tsne = TSNE(
        n_components=2,
        metric="precomputed",
        init="random",
        perplexity=20,
        random_state=42,
    )

    coords = tsne.fit_transform(dist_matrix)

    coords_df = pd.DataFrame(coords, columns=["x", "y"])
    coords_df["card"] = cards
    return coords_df


# --------------------------------------------------
# 5. Plot
# --------------------------------------------------
def plot_card_map(coords_df):
    plt.figure(figsize=(12, 12))
    plt.scatter(coords_df["x"], coords_df["y"], s=25)

    dx, dy = 0.1, 0.1  # Abstand der Labels vom Punkt (anpassen)

    for _, row in coords_df.iterrows():
        plt.text(
            row["x"] + dx,
            row["y"] + dy,
            row["card"],
            fontsize=7,
            alpha=0.85
        )

    plt.title("t-SNE Karten-Map (Co-Occurrence)")
    plt.axis("off")
    plt.tight_layout()
    plt.show()


# --------------------------------------------------
# Main
# --------------------------------------------------
if __name__ == "__main__":
    battles = load_battles()
    decks = extract_decks(battles)
    df = build_one_hot(decks)

    coords_df = build_card_map(df)
    plot_card_map(coords_df)

