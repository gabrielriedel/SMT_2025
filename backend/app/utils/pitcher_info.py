import duckdb as db 
import pandas as pd
import os
import numpy as np


DB_PATH = "/var/data/smt_2025.db" if os.path.exists("/var/data/smt_2025.db") else "database/smt_2025.db"

def get_pitchers(team: str):
    with db.connect(DB_PATH) as con:
        team_pitcher_df = con.sql(f"""SELECT DISTINCT pitcher 
                                        FROM game_info  
                                        WHERE CONTAINS (pitcher, '{team}');""").df()
        df_pitcher_hand = con.sql("""WITH rp AS 
                            (SELECT * FROM
                            (SELECT ball_position_x, play_id, game_str,
                            DENSE_RANK() OVER (PARTITION BY game_str, play_id ORDER BY timestamp) AS rank
                            FROM ball_pos bp) AS subquery
                            WHERE rank = 1), 

                            pitcher_rp AS (
                            SELECT rp.game_str, rp.ball_position_x, pitcher 
                            FROM rp
                            LEFT JOIN game_info gi
                            ON rp.game_str = gi.game_str AND rp.play_id = gi.play_per_game)
                            
                            SELECT AVG(ball_position_x) avg_rel_point, pitcher FROM pitcher_rp
                            GROUP BY pitcher;""").df()
        df_pitcher_hand["pitcher_hand"] = np.where(df_pitcher_hand["avg_rel_point"] > 0, "Left", "Right")
        team_pitcher_df = pd.merge(team_pitcher_df, df_pitcher_hand, on="pitcher", how="left")
        return team_pitcher_df
    
def get_pitcher_counts(pitcher: str):
    df_pitchers = get_all_pitcher_data()
    return df_pitchers[df_pitchers["pitcher"] == pitcher]

def get_all_pitcher_data():
    with db.connect(DB_PATH) as con:
        df_games_played = con.sql("""SELECT COUNT(DISTINCT game_str) AS games_played, pitcher
                                  FROM game_info
                                  GROUP BY pitcher
                                  ORDER BY COUNT(*) DESC;""").df()
        df_pickoff_counts = con.sql("""SELECT COUNT(*) AS pickoffs, pitcher
                            FROM (SELECT * FROM game_events ge
                            LEFT JOIN game_info gi
                            ON ge.game_str = gi.game_str AND ge.play_per_game = gi.play_per_game
                            WHERE event_code = 6) subquery
                            GROUP BY pitcher
                            ORDER BY COUNT(*) DESC;""").df()
        df_pitches_thrown = con.sql("""SELECT COUNT(*) AS pitches, pitcher
                                    FROM game_info
                                    GROUP BY pitcher
                                    ORDER BY COUNT(*) DESC;""").df()

 
    df_pitchers = pd.merge(df_pitches_thrown, df_pickoff_counts, on="pitcher", how = "left")
    df_pitchers = pd.merge(df_pitchers, df_games_played, on="pitcher", how = "left")
    df_pitchers["pickoffs"] = df_pitchers["pickoffs"].fillna(0)
    df_pitchers = df_pitchers[df_pitchers["games_played"] > 1]
    df_pitchers["picks_per_game"] = df_pitchers["pickoffs"]/df_pitchers["games_played"]

    return df_pitchers