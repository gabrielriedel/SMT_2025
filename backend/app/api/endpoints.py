import os
from fastapi import APIRouter, Response, HTTPException
import base64

router = APIRouter()

@router.get("/api/pitch_agg_stats", tags=["agg_stats"])
def get_pitch_scout_stats(team_name: str, pitcher: str):
    if not pitcher or not team_name:
        raise HTTPException(status_code=400, detail="Missing pitcher or team parameter")
    
    team_df = cache.get_team_data(team_name)

    try:
        stats = agg_stats.pitcher_agg_stats(pitcher, team_df)
        return {"pitcher": pitcher, "stats": stats}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating stats: {str(e)}")

@router.get("/api/team_names", tags=["roster"])
def get_all_team_names():
    try:
        df = cache.get_all_team_names()
        team_data = df.to_dict(orient="records")  # List of row-wise dicts
        return {"teams": team_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching team names: {str(e)}")

@router.get("/api/pitcher_names", tags=["roster"])
def get_pitcher_names(team_name: str):
    if not team_name:
        raise HTTPException(status_code=400, detail="Missing team_name parameter")
    
    try:
        pitcher_names = cache.get_pitcher_names(team_name)
        return {"pitcher_names": pitcher_names.tolist()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching pitcher names: {str(e)}")