import pandas as pd
from collections import Counter
import os

# --- Load clustered decks ---
script_dir = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(script_dir, 'decks_clustered.csv'))

# Group by cluster_id
cluster_groups = df.groupby('cluster_id')

output_lines = []
output_lines.append("cluster_id,core_and_tech,num_decks")

for cluster_id, group in cluster_groups:
    num_decks = len(group)
    if num_decks < 3:
        continue  # Skip clusters with fewer than 3 deck variants

    decks = []
    for _, row in group.iterrows():
        cards = [row[f'card_{i}'] for i in range(1, 9)]
        decks.append(set(cards))

    # Compute strict intersection (core)
    core = set(decks[0])
    for deck in decks[1:]:
        core &= deck

    if len(core) >= 6:
        core_cards = sorted(core)
        tech_pool = set()
        for deck in decks:
            tech_pool.update(deck - core)
        tech_cards = sorted(tech_pool)
    else:
        # Fallback: most common 6 cards
        all_cards = [card for deck in decks for card in deck]
        common = Counter(all_cards).most_common(6)
        core_cards = sorted([card for card, _ in common])
        core_set = set(core_cards)
        tech_pool = set(all_cards) - core_set
        tech_cards = sorted(tech_pool)

    core_str = "core: " + "; ".join(core_cards)
    tech_str = "tech: " + "; ".join(tech_cards)
    combined = f"{core_str},{tech_str}"

    output_lines.append(f"{cluster_id},{combined},{num_decks}")

# Write to CSV
output_path = os.path.join(script_dir, 'cluster_cores_and_tech_filtered.csv')
with open(output_path, 'w', encoding='utf-8') as f:
    for line in output_lines:
        f.write(line + "\n")

print("Saved filtered cluster cores & tech to:", output_path)
print("Total clusters (with >=3 deck variants):", len(output_lines) - 1)