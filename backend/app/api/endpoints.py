from fastapi import APIRouter, Response, HTTPException
from backend.animation.Animation import plot_animation
from app.utils import viz
import duckdb as db
import pandas as pd

router = APIRouter()

@router.get("/api/play_animation", tags=["visuals"])
def get_play_animation():
    try:
        df_pick = pd.read_csv("../../database/pickoff_plays.csv")
        viz.random_play(df_pick)
        
        return {"pitcher": pitcher, "stats": stats}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating play: {str(e)}")