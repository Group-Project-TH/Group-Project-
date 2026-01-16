import pandas as pd
import os
from collections import defaultdict, deque

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(script_dir, 'decks_cleaned.csv')

# Load the cleaned decks
df = pd.read_csv(input_path)

# Convert each deck to a frozenset of its 8 cards
deck_sets = []
for idx, row in df.iterrows():
    cards = frozenset(row[1:9])  # card_1 to card_8
    deck_sets.append((idx, cards))

n = len(deck_sets)
print(f"Loaded {n} decks.")

# Build adjacency list: connect decks that share ≥6 cards
adj = defaultdict(list)

# Extract lists for speed
indices = [i for i, _ in deck_sets]
sets = [s for _, s in deck_sets]

print("Building similarity graph... (this may take 1-2 minutes)")
for i in range(n):
    set_i = sets[i]
    for j in range(i + 1, n):
        if len(set_i & sets[j]) >= 6:
            adj[i].append(j)
            adj[j].append(i)

print("Finding connected components (clusters)...")
visited = [False] * n
cluster_id = [-1] * n
current_cluster = 0

for i in range(n):
    if not visited[i]:
        queue = deque([i])
        visited[i] = True
        while queue:
            node = queue.popleft()
            cluster_id[node] = current_cluster
            for neighbor in adj[node]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    queue.append(neighbor)
        current_cluster += 1

print(f"Found {current_cluster} clusters.")

# Add cluster_id to DataFrame
df['cluster_id'] = cluster_id

# Save result
output_path = os.path.join(script_dir, 'decks_clustered.csv')
df.to_csv(output_path, index=False)

print(f"Saved clustered decks to: {output_path}")