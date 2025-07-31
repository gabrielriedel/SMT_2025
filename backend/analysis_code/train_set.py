import duckdb as db
import pandas as pd
import numpy as np
from sklearn.model_selection import *

class TrainSet:

    def find_model_data():
        """
        A function that engineers features and creates a training dataset for the pickoff 
        likelihood model. 

        Features engineered:

        - Pitcher Handedness
        - Batter Handedness
        - Run Differential
        - Outs
        - Steal Score
        - Home Team
        - Runner Distance From Base
        
        Returns:

        Two Pandas DataFrames:
            - One DF of the features of the model
            - One Df (technically a series) of the target variable of the model
            
        """

        with db.connect("database/smt_2025.db") as con:
            # Find all unique baserunners who have been on first base
            players_on_first = con.sql("""SELECT DISTINCT first_baserunner AS player_name FROM game_info""").df()

            # Find the number of times each distinct baserunner as been on first base
            plays_on_first = con.sql("""SELECT COUNT(*) count_on_first, first_baserunner AS player_name FROM game_info 
                                        WHERE first_baserunner != 'NA' AND second_baserunner = 'NA' 
                                            AND third_baserunner = 'NA'
                                        GROUP BY first_baserunner
                                        ORDER BY COUNT(*) DESC""").df()
            # Find all plays with a runner on first attempting to steal second.
            steal_plays = con.sql("""WITH pitches AS (SELECT * FROM 
                                (SELECT *, 
                                LEAD(event_code) OVER (PARTITION BY game_str, play_per_game ORDER BY timestamp, event_code) AS next_event,
                            LEAD(player_position) OVER (PARTITION BY game_str, play_per_game ORDER BY timestamp, event_code) AS next_player
                                FROM game_events) subquery
                                WHERE event_code = 3 AND player_position = 2 AND (next_event = 2 OR next_event = 16) AND (next_player = 4 OR next_player = 6 OR next_player = 255)
                                ORDER BY game_str, play_per_game),
                            
                            runner_info AS (SELECT * FROM 
                            game_info
                                WHERE first_baserunner != 'NA' AND second_baserunner = 'NA')
                            
                            SELECT pi.game_str, play_id, pi.play_per_game, player_position, event_code, pi.home_team, first_baserunner as player_name, second_baserunner FROM pitches pi
                                INNER JOIN runner_info ri
                                ON pi.game_str = ri.game_str AND pi.play_per_game = ri.play_per_game
                            """).df()
            
            # Find stolen base attemps for each baserunner
            steal_count = con.sql("""WITH pitches AS (SELECT * FROM 
                                (SELECT *, 
                                LEAD(event_code) OVER (PARTITION BY game_str, 
                                play_per_game ORDER BY timestamp, 
                                event_code) AS next_event,
                            LEAD(player_position) OVER (PARTITION BY game_str, 
                                play_per_game ORDER BY timestamp, 
                                event_code) AS next_player
                                FROM game_events) subquery
                                WHERE event_code = 3 
                                AND player_position = 2 
                                AND (next_event = 2 OR next_event = 16) 
                                AND (next_player = 4 OR next_player = 6 OR next_player = 255)
                                ORDER BY game_str, play_per_game),
                            
                            runner_info AS (SELECT * 
                                FROM game_info
                                WHERE first_baserunner != 'NA' AND second_baserunner = 'NA')
                            
                            SELECT COUNT(*) stolen_bases, player_name FROM
                                (SELECT pi.game_str, play_id, pi.play_per_game, player_position, event_code, pi.home_team, first_baserunner as player_name, second_baserunner FROM pitches pi
                                INNER JOIN runner_info ri
                                ON pi.game_str = ri.game_str AND pi.play_per_game = ri.play_per_game) subquery
                            GROUP BY player_name
                            ORDER BY COUNT(*) DESC""").df()
            
            # Make table for each runner who has been on first along with their steal attempts and how many times they have been on first
            df_runners = pd.merge(players_on_first, plays_on_first, on = "player_name", how = "left")
            df_thieves = pd.merge(df_runners, steal_count, on="player_name", how="left").fillna(0).sort_values(by="stolen_bases", ascending=False)

            # Calculate a "steal_score" that rewards stolen base attempts and penalizes the more often a runner is on first base  
            df_thieves["steal_score_initial"] = (df_thieves["stolen_bases"]/df_thieves["count_on_first"] * np.log(df_thieves["stolen_bases"])).fillna(0)
            mean_score = df_thieves[df_thieves["steal_score_initial"] != 0]["steal_score_initial"].mean()
            df_thieves["steal_score"] = df_thieves["steal_score_initial"] / mean_score * 100

            # Find pickoff plays with a runner on first base
            df_pickoff_plays = con.sql("""
                                WITH first_base_player_pos AS (SELECT game_str, play_id, timestamp, player_position AS runner, field_x, field_y
                                    FROM(
                                        SELECT *, DENSE_RANK() OVER (PARTITION BY game_str, play_id ORDER BY timestamp) as time_order
                                        FROM player_pos 
                                        WHERE player_position = 11
                                        ORDER BY game_str, play_id, timestamp) sub1
                                        WHERE time_order = 1)
                                SELECT ge.game_str, ge.play_id, player_position, event_code, ge.home_team, top_bottom_inning, pitcher, batter, first_baserunner as player_name, field_x, field_y 
                                FROM game_events ge
                                LEFT JOIN game_info gi 
                                ON ge.game_str = gi.game_str AND ge.play_per_game = gi.play_per_game
                                INNER JOIN first_base_player_pos fb
                                ON ge.game_str = fb.game_str AND ge.play_id = fb.play_id
                                WHERE player_position = 1 AND event_code = 6 
                                    AND second_baserunner = 'NA' AND third_baserunner = 'NA' """).df()
            # Find plays that are pitches not pickoffs
            df_pitches = con.sql("""
                                WITH first_base_player_pos AS (SELECT game_str, play_id, timestamp, player_position AS runner, field_x, field_y
                                    FROM(
                                        SELECT *, DENSE_RANK() OVER (PARTITION BY game_str, play_id ORDER BY timestamp) as time_order
                                        FROM player_pos 
                                        WHERE player_position = 11
                                        ORDER BY game_str, play_id, timestamp) sub1
                                        WHERE time_order = 1)
                                SELECT ge.game_str, ge.play_id, player_position, event_code, ge.home_team, top_bottom_inning, pitcher, batter, first_baserunner as player_name, field_x, field_y 
                                FROM game_events ge
                                LEFT JOIN game_info gi 
                                ON ge.game_str = gi.game_str AND ge.play_per_game = gi.play_per_game
                                INNER JOIN first_base_player_pos fb
                                ON ge.game_str = fb.game_str AND ge.play_id = fb.play_id
                                WHERE player_position = 1 AND event_code = 1 
                                    AND second_baserunner = 'NA' AND third_baserunner = 'NA' 
                                """).df()
            # Signify pickoff vs. not pickoff
            df_pickoff_plays["pickoff"] = 1
            df_pitches["pickoff"] = 0

            # # Have the split of data where there are 'ratio' times as many regular pitches as pickoffs
            # df_pitches_model = df_pitches.sample(n=ratio*df_pickoff_plays.shape[0])

            # Concatenate pitch and pickoffs plays into one model dataset
            df_model_data = pd.concat((df_pickoff_plays, df_pitches), axis=0, join='inner', ignore_index=True, keys=None)

            # Find the distance of the runner from the front right corner of first base (3 seconds before pitch thrown)
            df_model_data["lead_distance"] = np.sqrt(pow(df_model_data["field_x"]-63.63, 2) + pow(df_model_data["field_y"]-63.63, 2)) - 1.25
            # Merge to add steal_score feature
            df_model_data = pd.merge(df_model_data, df_thieves, on="player_name", how = "left")
            # Binary is_home feature
            df_model_data["is_home"] = np.where(df_model_data['top_bottom_inning'] == "top", 1, 0)

            # Pitcher handedness: using the side of the y-axis to determine where the pitcher releases the ball
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
            # Categorize lefties with a '1' and righties with a '0'
            df_pitcher_hand["pitcher_hand"] = np.where(df_pitcher_hand["avg_rel_point"] > 0, 1, 0)
            df_model_data = pd.merge(df_model_data, df_pitcher_hand, on="pitcher", how="left")

            # Batter handedness: using the side of the y-axis to determine what box the hitter stands in
            df_batter_hand = con.sql("""WITH bh AS 
                            (SELECT * FROM
                            (SELECT field_x, play_id, game_str,
                            DENSE_RANK() OVER (PARTITION BY game_str, play_id ORDER BY timestamp) AS rank
                            FROM player_pos pp
                            WHERE player_position = 10) AS subquery
                            WHERE rank = 1),
                                
                            batter_rp AS (
                            SELECT bh.game_str, bh.field_x, batter 
                            FROM bh
                            LEFT JOIN game_info gi
                            ON bh.game_str = gi.game_str AND bh.play_id = gi.play_per_game)
                                
                            SELECT AVG(field_x) avg_stance, batter FROM batter_rp
                            GROUP BY batter""").df()
            
            # Categorize lefties with a '1' and righties with a '0'
            df_batter_hand["batter_hand"] = np.where(df_batter_hand["avg_stance"] > 0, 1, 0)
            df_model_data = pd.merge(df_model_data, df_batter_hand, on="batter", how="left")

            # Find the runs scored on each play and then calculate the current score/run differential of each game
            df_runs_per_play = con.sql(""" 
                        WITH run_scored AS (SELECT play_id, game_str, SUM(run) As runs FROM
                        (SELECT DISTINCT play_id, game_str, 
                        CASE 
                            WHEN (player_position = 11 AND abs(field_x) < 1 AND abs(field_y) < 1) THEN 1 
                            ELSE 0
                        END AS run          
                        FROM player_pos
                        UNION ALL
                        SELECT DISTINCT play_id, game_str, 
                        CASE 
                            WHEN (player_position = 12 AND abs(field_x) < 1 AND abs(field_y) < 1) THEN 1 
                            ELSE 0
                        END AS run
                        FROM player_pos
                        UNION ALL
                        SELECT DISTINCT play_id, game_str, 
                        CASE 
                            WHEN (player_position = 13 AND abs(field_x) < 1 AND abs(field_y) < 1) THEN 1 
                            ELSE 0
                        END AS run
                        FROM player_pos) subquery
                        GROUP BY game_str, play_id),
                                
                        run_plays AS (SELECT gi.game_str, runs, top_bottom_inning,
                        LEAD(play_per_game) OVER (PARTITION BY gi.game_str, top_bottom_inning ORDER BY play_per_game) AS play_per_game
                        FROM game_info gi
                        LEFT JOIN run_scored AS rs
                        ON rs.play_id = gi.play_per_game AND rs.game_str = gi.game_str)
                                
                        SELECT game_str, play_per_game, runs,
                            SUM(CASE WHEN top_bottom_inning = 'top' THEN runs ELSE 0 END)
                            OVER (PARTITION BY game_str ORDER BY play_per_game
                                ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS away_score,
                            SUM(CASE WHEN top_bottom_inning = 'bottom' THEN runs ELSE 0 END)
                                OVER (PARTITION BY game_str ORDER BY play_per_game
                                ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS home_score
                        FROM run_plays
                        ORDER BY game_str, play_per_game;""").df()
        
            df_runs_per_play["run_diff"] = df_runs_per_play["home_score"] - df_runs_per_play["away_score"]
            df_model_data = pd.merge(df_model_data, df_runs_per_play, left_on=['game_str', 'play_id'], right_on=['game_str', 'play_per_game'], how='left')

            # Find the number of outs recorded on a play --> how many outs there are in the inning on the next play 
            df_outs = con.sql("""WITH runner_info AS
                                    (SELECT *, 
                                    LAG(first_baserunner) OVER (PARTITION BY game_str, top_bottom_inning ORDER BY play_per_game) AS next_first,
                                    LAG(second_baserunner) OVER (PARTITION BY game_str, top_bottom_inning ORDER BY play_per_game) AS next_second,
                                    LAG(third_baserunner) OVER (PARTITION BY game_str, top_bottom_inning ORDER BY play_per_game) AS next_third
                                    FROM game_info)

                                    SELECT DISTINCT game_str, play_per_game, SUM(out) as outs
                                    FROM
                                    (SELECT game_str, top_bottom_inning, play_per_game, 
                                    CASE 
                                        WHEN first_baserunner NOT IN (next_first, next_second, next_third) THEN 1 
                                        ELSE 0
                                        END AS out
                                    FROM runner_info
                                    UNION ALL
                                    SELECT game_str, top_bottom_inning, play_per_game, 
                                    CASE 
                                        WHEN second_baserunner NOT IN (next_first, next_second, next_third) THEN 1 
                                        ELSE 0
                                        END AS out
                                    FROM runner_info
                                    UNION ALL
                                    SELECT game_str, top_bottom_inning, play_per_game, 
                                    CASE 
                                        WHEN third_baserunner NOT IN (next_first, next_second, next_third) THEN 1 
                                        ELSE 0
                                        END AS out
                                    FROM runner_info) subquery
                                    GROUP BY game_str, play_per_game
                                    """).df()
            
            df_outs["outs"] = np.where(df_outs["outs"] > 3, 0, df_outs["outs"])
            df_model_data = pd.merge(df_model_data, df_outs, left_on=['game_str', 'play_id'], right_on=['game_str', 'play_per_game'], how='left')

            # Remove rows with any NA values
            df_model_data = df_model_data.dropna()
            df_model_data.to_csv("model_dataset.csv")

            X = df_model_data[['outs','run_diff', 'pitcher_hand', 
                                    'batter_hand', 'lead_distance', 'steal_score', 'is_home'
                                    ]]
            y = df_model_data[["pickoff"]]

            return X, y

    def split_model_data(self, val_prop: int, test_prop: int):
            X, y = self.find_model_data()

            X_train_val, X_test, y_train_val, y_test = train_test_split(X, y, test_size=test_prop, stratify=y, random_state=1313)

            new_val_prop = val_prop / (1 - test_prop)
            print("new_val", new_val_prop)

            X_train, X_val, y_train, y_val = train_test_split(X_train_val, y_train_val, test_size=new_val_prop, stratify=y_train_val, random_state=42)

            return {"X": [X_train, X_val, X_test],
                    "y": [y_train, y_val, y_test]} 

TrainSet.find_model_data()