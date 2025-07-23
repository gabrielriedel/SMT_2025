from animation.Animation import plot_animation
import duckdb as db 
import pandas as pd
import os

def random_play(df):
    random_row = df.sample(n=1).reset_index(drop=True)
    DB_PATH = "/var/data/smt_2025.db" if os.path.exists("/var/data/smt_2025.db") else "database/smt_2025.db"
    with db.connect(DB_PATH) as con:
                    game_string = random_row["game_str"].iloc[0]
                    play_id = random_row["play_per_game"].iloc[0]
                    player_position_df = con.sql(f"""SELECT * FROM player_pos  
                                                    WHERE game_str = '{game_string}';""").df()
                    ball_position_df = con.sql(f"""SELECT * FROM ball_pos  
                                                    WHERE game_str = '{game_string}';""").df()
                    buf = plot_animation(player_position_df, ball_position_df, int(play_id), True)
                    return buf