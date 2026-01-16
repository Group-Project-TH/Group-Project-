##Ablauf wie man zum png kommt.
decks.csv und all_players_clean.csv war der Ausgangs punkt von Moritz.



decks.csv


    ↓ cleaner.py dublicate werden raus gemacht


decks_cleaned.csv 


    ↓ cluster.py decks werden in cluster eingeteilt 6/8 core karten und 2 tech optionen die varieren können


decks_clusterd.csv 


    ↓ clusterdecksnewinfo.py cluster werden zusammen gefügt in core decks die unter 3 mal vorkamen werden raus gefilter


cluster_cores_and_tech_filtered.csv einzelne geclusterte decks mit den jeweiligen karten und tech optionen keine dublicate



decks_clustered.csv + cluster_cores_and_tech_filtered.csv + all_players_clean.csv


                                        ↓ clusteravb.py  deckcluster vs deckcluster muss mindest 3 matches gegeneinaner haben rest wird rausgefilltert


                            cluster_matchup_counters.csv deckcluster vs deckcluster matches mit winrate und total games 



cluster_matchup_counters.csv


            ↓ clustervisualizer.py erstellung einer Heatmap clusterids werden auf x und y achse gemapt


        newplot.png



decks_clustered.csv + cluster_cores_and_tech_filtered.csv + all_players_clean.csv


                                    ↓ clusterperformance2.py findet die decks mit der höchsten winrate und dem höchsten avg_trophy_change


                        cluster_performance_with_cores.csv

                        
diese csv datei hat Moritz visualisiert 

