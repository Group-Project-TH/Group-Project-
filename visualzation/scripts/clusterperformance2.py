import pandas as pd
import csv
import ast
from collections import defaultdict
import os

def normalize_deck(card_list):
    return tuple(sorted(card_list))

script_dir = os.path.dirname(os.path.abspath(__file__))

# --- Step 1: Load deck-to-cluster mapping ---
deck_df = pd.read_csv(os.path.join(script_dir, 'decks_clustered.csv'))
deck_to_cluster = {}
for _, row in deck_df.iterrows():
    cards = [row[f'card_{i}'] for i in range(1, 9)]
    key = normalize_deck(cards)
    deck_to_cluster[key] = int(row['cluster_id'])

print(f"Loaded {len(deck_to_cluster)} deck-to-cluster mappings.")

# --- Step 2: Load filtered clusters (manual parse due to commas in data) ---
valid_cluster_ids = set()
cluster_info = {}  # cluster_id -> core_and_tech string

filtered_path = os.path.join(script_dir, 'cluster_cores_and_tech_filtered.csv')
with open(filtered_path, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith('cluster_id'):
            continue
        
        # Split into: cluster_id, core..., tech..., num_decks
        # Strategy: first field = cluster_id, last field = num_decks, middle = core_and_tech
        parts = line.split(',')
        if len(parts) < 3:
            continue
        
        try:
            cluster_id = int(parts[0])
            num_decks = int(parts[-1])
            core_and_tech = ','.join(parts[1:-1])  # everything in between
            valid_cluster_ids.add(cluster_id)
            cluster_info[cluster_id] = core_and_tech
        except ValueError:
            continue

print(f"Analyzing {len(valid_cluster_ids)} filtered clusters (>=3 deck variants).")

# --- Step 3: Parse battle data ---
records = []
input_path = os.path.join(script_dir, 'all_players_clean.csv')
with open(input_path, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        if len(row) < 5:
            continue
        try:
            player_list = ast.literal_eval(row[4])
        except:
            continue
        if not isinstance(player_list, list):
            continue
        for player in player_list:
            if not (isinstance(player, dict) and 'cards' in player and 'trophyChange' in player):
                continue
            cards = player['cards']
            if not (isinstance(cards, list) and len(cards) == 8):
                continue
            try:
                card_names = [card['name'] for card in cards if 'name' in card]
                if len(card_names) != 8:
                    continue
            except:
                continue
            tc = player.get('trophyChange')
            if tc is None:
                continue
            deck_key = normalize_deck(card_names)
            cid = deck_to_cluster.get(deck_key)
            if cid is not None and cid in valid_cluster_ids:
                records.append((cid, int(tc)))

print(f"Parsed {len(records)} matches belonging to filtered clusters.")

# --- Step 4: Aggregate performance ---
cluster_perf = defaultdict(list)
for cid, tc in records:
    cluster_perf[cid].append(tc)

results = []
for cid, changes in cluster_perf.items():
    n = len(changes)
    if n < 3:
        continue
    avg_trophy = sum(changes) / n
    win_rate = sum(1 for x in changes if x > 0) / n
    results.append({
        'cluster_id': cid,
        'core_and_tech': cluster_info[cid],
        'total_matches': n,
        'avg_trophy_change': round(avg_trophy, 2),
        'win_rate_pct': round(win_rate * 100, 1)
    })

# --- Step 5: Save final result ---
if results:
    # Sort by trophy gain
    results.sort(key=lambda x: x['avg_trophy_change'], reverse=True)
    
    output_path = os.path.join(script_dir, 'cluster_performance_with_cores.csv')
    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['cluster_id', 'core_and_tech', 'total_matches', 'avg_trophy_change', 'win_rate_pct'])
        for r in results:
            writer.writerow([
                r['cluster_id'],
                r['core_and_tech'],
                r['total_matches'],
                r['avg_trophy_change'],
                r['win_rate_pct']
            ])
    
    print(f"\nSaved performance data for {len(results)} clusters to:")
    print(output_path)
else:
    print("No filtered clusters met the match threshold (>=3 matches).")