## Ablauf: Wie man zum PNG kommt

decks.csv und all_players_clean.csv war der Ausgangspunkt von Moritz.

decks.csv  
 ↓ cleaner.py → duplicate werden raus gemacht  
decks_cleaned.csv  
 ↓ cluster.py → decks werden in cluster eingeteilt (6/8 core Karten + 2 tech Optionen)  
decks_clusterd.csv  
 ↓ clusterdecksnewinfo.py → cluster werden zusammen gefügt; unter 3 mal vorkommende werden raus gefiltert  
cluster_cores_and_tech_filtered.csv → einzelne geclusterte Decks mit Karten und Tech-Optionen (keine Duplicates)

decks_clustered.csv + cluster_cores_and_tech_filtered.csv + all_players_clean.csv  
 ↓ clusteravb.py → deckcluster vs deckcluster muss mindestens 3 Matches haben → rest wird rausgefiltert  
cluster_matchup_counters.csv → deckcluster vs deckcluster matches mit winrate und total games 

cluster_matchup_counters.csv  
 ↓ clustervisualizer.py → Erstellung einer Heatmap; clusterids werden auf x und y Achse gemapt  
newplot.png

decks_clustered.csv + cluster_cores_and_tech_filtered.csv + all_players_clean.csv  
                                ↓ clusterperformance2.py → findet die Decks mit der höchsten Winrate und dem höchsten avg_trophy_change  
cluster_performance_with_cores.csv → dies CSV-Datei hat Moritz visualisiert