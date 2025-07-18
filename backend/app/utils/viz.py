from animation.Animation import plot_animation
import duckdb as db 
import pandas as pd

def random_play(df):
    random_row = df.sample(n=1).reset_index(drop=True)
    with db.connect("database/smt_2025.db") as con:
        try:
                game_string = random_row["game_str"].iloc[0]
                print(game_string)
                play_id = random_row["play_per_game"].iloc[0]
                player_position_df = con.sql(f"""SELECT * FROM player_pos  
                                                WHERE game_str = '{game_string}';""").df()
                ball_position_df = con.sql(f"""SELECT * FROM ball_pos  
                                                WHERE game_str = '{game_string}';""").df()
                plot_animation(player_position_df, ball_position_df, int(play_id), True)
        except:
             random_play(df)
    
    return [game_string, play_id]