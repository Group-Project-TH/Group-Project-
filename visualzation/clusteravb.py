# best
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

# --- Step 2: Load filtered clusters (manual parse) ---
valid_cluster_ids = set()
cluster_info = {}

filtered_path = os.path.join(script_dir, 'cluster_cores_and_tech_filtered.csv')
with open(filtered_path, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith('cluster_id'):
            continue
        parts = line.split(',')
        if len(parts) < 3:
            continue
        try:
            cluster_id = int(parts[0])
            core_and_tech = ','.join(parts[1:-1])
            valid_cluster_ids.add(cluster_id)
            cluster_info[cluster_id] = core_and_tech
        except ValueError:
            continue

print(f"Analyzing {len(valid_cluster_ids)} filtered clusters.")

# --- Step 3: Parse battles (two player columns: index 4 and 5) ---
wins = defaultdict(lambda: defaultdict(int))
total_matchups = defaultdict(lambda: defaultdict(int))
battle_count = 0

input_path = os.path.join(script_dir, 'all_players_clean.csv')
with open(input_path, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        if len(row) < 6:
            continue
        
        # Parse player 1 from column 4
        try:
            p1_list = ast.literal_eval(row[4])
            if not isinstance(p1_list, list) or len(p1_list) != 1:
                continue
            player1 = p1_list[0]
        except:
            continue

        # Parse player 2 from column 5
        try:
            p2_list = ast.literal_eval(row[5])
            if not isinstance(p2_list, list) or len(p2_list) != 1:
                continue
            player2 = p2_list[0]
        except:
            continue

        players = []
        for player in [player1, player2]:
            if not isinstance(player, dict):
                break
            if 'cards' not in player or 'trophyChange' not in player:
                break
            cards = player['cards']
            if not (isinstance(cards, list) and len(cards) == 8):
                break
            try:
                card_names = [card['name'] for card in cards if 'name' in card]
                if len(card_names) != 8:
                    break
            except:
                break
            tc = player.get('trophyChange')
            if tc is None:
                break
            deck_key = normalize_deck(card_names)
            cid = deck_to_cluster.get(deck_key)
            if cid is None or cid not in valid_cluster_ids:
                break
            players.append((cid, tc))
        else:
            if len(players) == 2:
                (cid1, tc1), (cid2, tc2) = players
                if tc1 > tc2:
                    winner, loser = cid1, cid2
                elif tc2 > tc1:
                    winner, loser = cid2, cid1
                else:
                    continue  # draw or invalid
                wins[winner][loser] += 1
                total_matchups[winner][loser] += 1
                total_matchups[loser][winner] += 1
                battle_count += 1

print(f"Processed {battle_count} valid cluster-vs-cluster battles.")

# --- Step 4: Compute win rates (min 3 games per pair) ---
matchup_results = []
for cid_a in valid_cluster_ids:
    for cid_b in valid_cluster_ids:
        if cid_a >= cid_b:
            continue
        total = total_matchups[cid_a][cid_b]
        if total < 3:
            continue
        wins_a = wins[cid_a][cid_b]
        wins_b = wins[cid_b][cid_a]
        winrate_a_vs_b = wins_a / total
        winrate_b_vs_a = wins_b / total
        matchup_results.append({
            'cluster_a': cid_a,
            'cluster_b': cid_b,
            'a_vs_b_winrate_pct': round(winrate_a_vs_b * 100, 1),
            'b_vs_a_winrate_pct': round(winrate_b_vs_a * 100, 1),
            'total_games': total
        })

# Sort by how well A does against B (descending)
matchup_results.sort(key=lambda x: x['a_vs_b_winrate_pct'], reverse=True)

# --- Step 5: Save results ---
if matchup_results:
    output_path = os.path.join(script_dir, 'cluster_matchup_counters.csv')
    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            'cluster_a', 'core_a',
            'cluster_b', 'core_b',
            'a_vs_b_winrate_pct', 'b_vs_a_winrate_pct', 'total_games'
        ])
        for r in matchup_results:
            writer.writerow([
                r['cluster_a'],
                cluster_info.get(r['cluster_a'], ''),
                r['cluster_b'],
                cluster_info.get(r['cluster_b'], ''),
                r['a_vs_b_winrate_pct'],
                r['b_vs_a_winrate_pct'],
                r['total_games']
            ])
    
    # Use plain text (no emoji) to avoid encoding errors
    print(f"\n[SUCCESS] Saved {len(matchup_results)} matchups to:")
    print(output_path)

    print("\nTop 5 Counter Matchups (Cluster A vs Cluster B):")
    print("Format: Cluster A wins X% of the time against Cluster B")
    for r in matchup_results[:5]:
        print(f"Cluster {r['cluster_a']} vs {r['cluster_b']}: {r['a_vs_b_winrate_pct']}% win ({r['total_games']} games)")
else:
    print("Not enough data for reliable analysis (need >=3 games per pair).")
