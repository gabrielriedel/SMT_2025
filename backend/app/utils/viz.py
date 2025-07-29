from animation.Animation import plot_animation
import duckdb as db 
import pandas as pd
import os
from plotnine import *
from io import BytesIO

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

def get_pickoff_counts_hist(df_pitchers: pd.DataFrame, count: int, pitcher: str):
        binwidth = 1
        df_pitchers['bin'] = (df_pitchers['pickoffs'] // binwidth) * binwidth
        target_bin = (count // binwidth) * binwidth
        print(target_bin)
        df_pitchers['highlight'] = df_pitchers['bin'] == target_bin.iloc[0]

        plot = ggplot(df_pitchers, aes(x='pickoffs', fill='highlight')) \
        + geom_histogram(binwidth=binwidth, color="black", boundary=0) \
        + scale_fill_manual(values={True: "green", False: "black"},
            name='Pitcher Highlight',                  \
            labels=['Other', f'{pitcher}']) \
        + labs(title = "Number of Pickoffs by Each Pitcher (min. 2 games played)",
            x="Pickoff Count",
            y="Number of Pitchers") \
        + theme_classic()
        buf = BytesIO()
        plot.save(buf, format='png', verbose=False)
        buf.seek(0)
        return buf

def get_pitch_counts_hist(df_pitchers: pd.DataFrame, count: int, pitcher: str):
        binwidth = 100
        df_pitchers['bin'] = (df_pitchers['pitches'] // binwidth) * binwidth
        target_bin = (count // binwidth) * binwidth
        df_pitchers['highlight'] = df_pitchers['bin'] == target_bin.iloc[0]

        plot = ggplot(df_pitchers, aes(x='pitches', fill='highlight')) \
        + geom_histogram(binwidth=binwidth, color="black", boundary=0) \
        + scale_fill_manual(values={True: "green", False: "black"},
            name='Pitcher Highlight',                  \
            labels=['Other', f'{pitcher}']) \
        + labs(title = "Number of Pitches by Each Pitcher (min. 2 games played)",
            x="Pitch Count",
            y="Number of Pitchers") \
        + theme_classic()
        buf = BytesIO()
        plot.save(buf, format='png', verbose=False)
        buf.seek(0)
        return buf

def get_games_played_hist(df_pitchers: pd.DataFrame, count: int, pitcher: str):
        binwidth = 2
        df_pitchers['bin'] = (df_pitchers['games_played'] // binwidth) * binwidth
        target_bin = (count // binwidth) * binwidth
        df_pitchers['highlight'] = df_pitchers['bin'] == target_bin.iloc[0]

        plot = ggplot(df_pitchers, aes(x='games_played', fill='highlight')) \
        + geom_histogram(binwidth=binwidth, color="black", boundary=0) \
        + scale_fill_manual(values={True: "green", False: "black"},
            name='Pitcher Highlight',                  \
            labels=['Other', f'{pitcher}']) \
        + labs(title = "Number of Games Played by Each Pitcher (min. 2 games played)",
            x="Game Count",
            y="Number of Pitchers") \
        + theme_classic()
        buf = BytesIO()
        plot.save(buf, format='png', verbose=False)
        buf.seek(0)
        return buf

def get_ppg_hist(df_pitchers: pd.DataFrame, count: int, pitcher: str):
        binwidth = 0.2
        df_pitchers['bin'] = (df_pitchers['picks_per_game'] // binwidth) * binwidth
        target_bin = (count // binwidth) * binwidth
        df_pitchers['highlight'] = df_pitchers['bin'] == target_bin.iloc[0]
        plot = ggplot(df_pitchers, aes(x='picks_per_game', fill='highlight')) \
        + geom_histogram(binwidth=binwidth, color="black", boundary=0) \
        + scale_fill_manual(values={True: "green", False: "black"},
            name='Pitcher Highlight',                  \
            labels=['Other', f'{pitcher}']) \
        + labs(title = "Pickoffs per Game by Each Pitcher (min. 2 games played)",
            x="Pickoffs per Game",
            y="Number of Pitchers") \
        + theme_classic()
        buf = BytesIO()
        plot.save(buf, format='png', verbose=False)
        buf.seek(0)
        return buf
