import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# -----------------------------
# Daten laden
# -----------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
BASE_DIR = SCRIPT_DIR.parent

DATA_PATH = BASE_DIR / "data" / "cluster_performance_with_cores.csv"
df = pd.read_csv(DATA_PATH)

# Cluster, die du plotten willst
clusters_of_interest = [0, 1, 2, 3, 4, 5, 6, 7, 12, 16, 21, 30, 40]

deck_names = {
    0: "Giant Sparky",
    1: "Balloon Freeze",
    2: "Cycle",
    3: "E-Giant",
    4: "Goblin Giant Pekka",
    5: "Hyper B8",
    6: "Bridge Spam",
    7: "BalloonMiner",
    12: "Royal Giant",
    16: "Elixir Golem Heal",
    21: "Elixir Golem",
    30: "Fireball B8",
    40: "LavaLoon"
}

# Filtern + sortieren
df_filt = df[df["cluster_id"].isin(clusters_of_interest)].copy()
df_filt = df_filt.sort_values("cluster_id")

# -----------------------------
# Plot: Winrate vs Spielanzahl
# -----------------------------
plt.figure(figsize=(10, 6))
plt.scatter(df_filt["total_matches"], df_filt["win_rate_pct"], s=60)

plt.xlabel("Anzahl Spiele (total_matches)")
plt.ylabel("Winrate (%) (win_rate_pct)")
plt.title("Winrate vs. Anzahl Spiele pro Cluster")

# Labels (Deck-Name) an die Punkte schreiben
for _, row in df_filt.iterrows():
    cid = int(row["cluster_id"])
    label = deck_names.get(cid, str(cid))

    plt.text(
        row["total_matches"] + 2,     # kleiner x-Offset
        row["win_rate_pct"] + 0.2,    # kleiner y-Offset
        label,
        fontsize=9
    )
plt.tight_layout()
plt.show()
