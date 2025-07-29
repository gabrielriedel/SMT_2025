import duckdb as db 
import pandas as pd
import os

def get_pitchers(team: str):
    DB_PATH = "/var/data/smt_2025.db" if os.path.exists("/var/data/smt_2025.db") else "database/smt_2025.db"
    with db.connect(DB_PATH) as con:
        team_pitcher_df = con.sql(f"""SELECT DISTINCT pitcher 
                                        FROM game_info  
                                        WHERE CONTAINS (pitcher, '{team}');""").df()
        return team_pitcher_df["pitcher"]