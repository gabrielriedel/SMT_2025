from fastapi import APIRouter, Response, HTTPException
from app.utils import viz, pitcher_info
import duckdb as db
import pandas as pd
import os

router = APIRouter()

@router.get("/api/pick_animation", tags=["visuals"])
def get_play_animation():
    try:
        df_pick = pd.read_csv("database/pickoff_plays.csv")
        buf = viz.random_play(df_pick)

        return Response(content=buf.read(), media_type="image/gif")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating play: {str(e)}")
@router.get("/api/steal_animation", tags=["visuals"])
def get_play_animation():
    try:
        df_steal = pd.read_csv("database/steal_plays.csv")
        buf = viz.random_play(df_steal)

        return Response(content=buf.read(), media_type="image/gif")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating play: {str(e)}")
@router.get("/api/run_animation", tags=["visuals"])
def get_play_animation():
    try:
        df_steal = pd.read_csv("database/run_plays.csv")
        buf = viz.random_play(df_steal)

        return Response(content=buf.read(), media_type="image/gif")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating play: {str(e)}")
    
@router.get("/api/out_animation", tags=["visuals"])
def get_play_animation():
    try:
        df_steal = pd.read_csv("database/out_plays.csv")
        buf = viz.random_play(df_steal)

        return Response(content=buf.read(), media_type="image/gif")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating play: {str(e)}")
    
@router.get("/api/pitcher_names", tags=["scouting"])
def get_pitchers_by_team(team: str):
    try:
        pitchers = pitcher_info.get_pitchers(team).tolist()
        return {"pitchers": pitchers}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching pitcher names: {str(e)}")

        