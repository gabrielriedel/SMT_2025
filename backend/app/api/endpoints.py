from fastapi import APIRouter, Response, HTTPException
from backend.animation.Animation import plot_animation
import duckdb as db
import pandas as pd

router = APIRouter()

@router.get("/api/play_animation", tags=["visuals"])
def get_play_animation():
    try:
        df_pick = pd.read_csv("../../database/pickoff_plays.csv")
        random_row = df_pick.sample(n=1)
        with db.connect("smt_2025.db") as con:
                print(random_row["game_str"])
                player_position_df = con.sql(f"""SELECT * FROM player_pos  
                                                WHERE game_str = {random_row["game_str"].astype(str)};""").df()
                ball_position_df = con.sql(f"""SELECT * FROM ball_pos  
                                                WHERE game_str = {random_row["game_str"]};""").df()
                plot_animation(player_position_df, ball_position_df, random_row["play_id"], False)
        return {"pitcher": pitcher, "stats": stats}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating play: {str(e)}")