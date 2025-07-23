from fastapi import APIRouter, Response, HTTPException
from app.utils import viz
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
@router.get("/api/debug_file")
def debug_file():
    try:
        DB_PATH = "/var/data/smt_2025.db" if os.path.exists("/var/data/smt_2025.db") else "database/smt_2025.db"
        exists = os.path.exists(DB_PATH)
        return {"exists": exists, "cwd": os.getcwd()}
    except Exception as e:
        return {"error": str(e)}