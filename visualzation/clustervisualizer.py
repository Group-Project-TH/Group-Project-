import pandas as pd
import plotly.graph_objects as go

# Load matchup data
df = pd.read_csv("cluster_matchup_counters.csv")

# Step 1: Get unique cluster_a values, sorted
unique_cluster_a = sorted(df["cluster_a"].unique())
print(f"Unique cluster_a IDs ({len(unique_cluster_a)}): {unique_cluster_a}")

# Step 2: Filter matchups: only those where cluster_a and cluster_b are in this list AND total_games >= 3
df_filtered = df[
    (df["cluster_a"].isin(unique_cluster_a)) &
    (df["cluster_b"].isin(unique_cluster_a)) &
    (df["total_games"] >= 3)
]

print(f"Matchups after filtering (>=3 games): {len(df_filtered)}")
print(f"Total games used: {df_filtered['total_games'].sum()}")

# Step 3: Create pivot table
heatmap_data = df_filtered.pivot(
    index="cluster_b",
    columns="cluster_a",
    values="a_vs_b_winrate_pct"
).reindex(index=unique_cluster_a, columns=unique_cluster_a)

# Step 4: Fill lower triangle with inverse win rates + diagonal = 50%
for i, b in enumerate(heatmap_data.index):
    for j, a in enumerate(heatmap_data.columns):
        if pd.isna(heatmap_data.loc[b, a]):
            if not pd.isna(heatmap_data.loc[a, b]):
                heatmap_data.loc[b, a] = 100 - heatmap_data.loc[a, b]
            elif a == b:
                heatmap_data.loc[b, a] = 50.0

# Step 5: Define deck names
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

x_labels = [deck_names.get(cid, f"Cluster {cid}") for cid in heatmap_data.columns]
y_labels = [deck_names.get(cid, f"Cluster {cid}") for cid in heatmap_data.index]

# Step 6: Build game count lookup
game_count_lookup = {}
for _, row in df_filtered.iterrows():
    game_count_lookup[(row['cluster_a'], row['cluster_b'])] = row['total_games']

# Step 7: Create hover text
hover_text = []
for b in heatmap_data.index:
    row = []
    for a in heatmap_data.columns:
        if pd.notna(heatmap_data.loc[b, a]):
            games = game_count_lookup.get((a, b), game_count_lookup.get((b, a), 0))
            if a == b:
                games = 0
            row.append(
                f"<b>{deck_names.get(a, f'Cluster {a}')}</b> vs <b>{deck_names.get(b, f'Cluster {b}')}</b><br>"
                f"Win Rate: {heatmap_data.loc[b, a]:.1f}%<br>"
                f"Games: {games}"
            )
        else:
            row.append("")
    hover_text.append(row)

# Step 8: Text labels (only where data exists)
text_data = heatmap_data.map(lambda x: f"{x:.1f}%" if pd.notna(x) else "").values

# Step 9: Build heatmap (use standard colorscale, NaN shows as white)
fig = go.Figure(data=go.Heatmap(
    z=heatmap_data.values,
    x=x_labels,
    y=y_labels,
    colorscale=[[0, "red"], [0.5, "white"], [1, "green"]],
    zmin=0,
    zmax=100,
    colorbar=dict(title="Win Rate (%)"),
    text=text_data,
    hoverinfo="text",
    hovertext=hover_text,
    texttemplate="%{text}",
    textfont={"size": 10},
))

# Layout
fig.update_layout(
    title=(
        "Clash Royale Cluster Matchup Heatmap<br>"
        "<sup>• Green = Win rate &gt;50% • Red = &lt;50% • Grey = Not enough data (&lt;3 games)</sup><br>"
        f"<sup>Total Games Used: {df_filtered['total_games'].sum()}</sup>"
    ),
    xaxis_title="Player Deck",
    yaxis_title="Opponent Deck",
    width=900,
    height=800,
    font=dict(size=12),
    xaxis=dict(tickangle=-45),
    yaxis=dict(autorange='reversed')
)

# Save and show
fig.write_html("cluster_heatmap_named.html")
print("Heatmap saved as 'cluster_heatmap_named.html'")
fig.show()