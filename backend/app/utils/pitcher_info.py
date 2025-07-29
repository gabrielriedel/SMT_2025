import duckdb as db 
import pandas as pd
import os


DB_PATH = "/var/data/smt_2025.db" if os.path.exists("/var/data/smt_2025.db") else "database/smt_2025.db"

def get_pitchers(team: str):
    with db.connect(DB_PATH) as con:
        team_pitcher_df = con.sql(f"""SELECT DISTINCT pitcher 
                                        FROM game_info  
                                        WHERE CONTAINS (pitcher, '{team}');""").df()
        return team_pitcher_df["pitcher"]
    
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