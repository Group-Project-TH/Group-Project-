import pandas as pd
import os

# Get directory of this script
script_dir = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(script_dir, 'decks.csv')
output_path = os.path.join(script_dir, 'decks_cleaned.csv')

# Load data
df = pd.read_csv(input_path)

# Define card columns
card_cols = [f'card_{i}' for i in range(1, 9)]

# Normalize: sort cards in each row
df[card_cols] = df[card_cols].apply(lambda row: sorted(row), axis=1, result_type='expand')

# Remove duplicates
df_clean = df.drop_duplicates(subset=card_cols).reset_index(drop=True)

# Optional: reset deck_id
df_clean['deck_id'] = df_clean.index

# Save
df_clean.to_csv(output_path, index=False)

print(f"Original decks: {len(df)}")
print(f"Unique decks  : {len(df_clean)}")
print(f"Saved to: {output_path}")