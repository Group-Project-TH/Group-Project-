import pandas as pd
from pathlib import Path

# ==================================================
# 1. Pfade sauber setzen
# ==================================================
SCRIPT_DIR = Path(__file__).resolve().parent
BASE_DIR = SCRIPT_DIR.parent

CLUSTERS_PATH = BASE_DIR / "data" / "cluster_cores_and_tech_filtered.csv"
DECKS_PATH    = BASE_DIR / "data" / "opponent_decks_cleaned.csv"


print("Cluster-Datei gefunden:", CLUSTERS_PATH.exists())
print("Deck-Datei gefunden:", DECKS_PATH.exists())

clusters_df = pd.read_csv(CLUSTERS_PATH)
decks_df    = pd.read_csv(DECKS_PATH)

# ==================================================
# 2. Hilfsfunktion: Karten-String -> Liste
# ==================================================
def split_cards(card_string):
    if pd.isna(card_string):
        return []

    s = str(card_string)

    # Präfixe entfernen
    s = s.replace("core:", "").replace("tech:", "")

    return [c.strip() for c in s.split(";") if c.strip()]


# ==================================================
# 3. Cluster aufbauen
# ==================================================
print("Cluster-Spalten:", clusters_df.columns.tolist())


CORE_COL = "core"
TECH_COL = "tech"

clusters = []

for _, row in clusters_df.iterrows():
    clusters.append({
        "cluster_id": row["cluster_id"],
        "core": split_cards(row[CORE_COL]),
        "tech": split_cards(row[TECH_COL])
    })

print("Beispiel-Cluster:", clusters[0])

# ==================================================
# 4. Decks aufbauen (jede Karte = eigene Spalte)
# ==================================================
print("Deck-Spalten:", decks_df.columns.tolist())

# Alle Karten-Spalten automatisch erkennen
card_columns = [
    c for c in decks_df.columns
    if c.lower().startswith("card") or c.lower().startswith("slot")
]

print("Erkannte Karten-Spalten:", card_columns)

decks = []

for idx, row in decks_df.iterrows():
    cards = [
        str(row[col]).strip()
        for col in card_columns
        if pd.notna(row[col])
    ]

    decks.append({
        "deck_id": idx,
        "cards": cards
    })

print("Beispiel-Deck:", decks[0])

# ==================================================
# 5. Matching-Funktion
# ==================================================
def cluster_matches_deck(deck_cards, cluster, min_tech=2):
    deck_set = set(deck_cards)

    core_set = set(cluster["core"])
    tech_set = set(cluster["tech"])

    if not core_set.issubset(deck_set):
        return False

    return len(deck_set & tech_set) >= min_tech

# ==================================================
# 6. Cluster in ALLEN Decks suchen
# ==================================================
matches = []

for deck in decks:
    for cluster in clusters:
        if cluster_matches_deck(deck["cards"], cluster):
            matches.append({
                "deck_id": deck["deck_id"],
                "cluster_id": cluster["cluster_id"]
            })

matches_df = pd.DataFrame(matches)

print("\nGefundene Matches (erste Zeilen):")
print(matches_df.head())

# ==================================================
# 7. Cluster-Häufigkeit
# ==================================================
cluster_counts = (
    matches_df
    .groupby("cluster_id")
    .size()
    .reset_index(name="deck_count")
    .sort_values("deck_count", ascending=False)
)

print("\nCluster-Häufigkeit:")
print(cluster_counts)

# ==================================================
# 8.  Ergebnisse speichern
# ==================================================
matches_df.to_csv(BASE_DIR / "cluster_matches_in_opponent_decks.csv", index=False)
cluster_counts.to_csv(BASE_DIR / "cluster_frequency.csv", index=False)

