from fastapi import APIRouter, Response, HTTPException
from app.utils import viz, pitcher_info as pi
import pandas as pd
import joblib
import numpy as np

router = APIRouter()

@router.get("/api/pick_animation", tags=["visuals"])
def get_pick_animation():
    try:
        df_pick = pd.read_csv("database/pickoff_plays.csv")
        buf = viz.random_play(df_pick)

        return Response(content=buf.read(), media_type="image/gif")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating play: {str(e)}")
@router.get("/api/steal_animation", tags=["visuals"])
def get_steal_animation():
    try:
        df_steal = pd.read_csv("database/steal_plays.csv")
        buf = viz.random_play(df_steal)

        return Response(content=buf.read(), media_type="image/gif")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating play: {str(e)}")
@router.get("/api/run_animation", tags=["visuals"])
def get_run_animation():
    try:
        df_steal = pd.read_csv("database/run_plays.csv")
        buf = viz.random_play(df_steal)

        return Response(content=buf.read(), media_type="image/gif")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating play: {str(e)}")
    
@router.get("/api/out_animation", tags=["visuals"])
def get_out_animation():
    try:
        df_steal = pd.read_csv("database/out_plays.csv")
        buf = viz.random_play(df_steal)

        return Response(content=buf.read(), media_type="image/gif")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating play: {str(e)}")
    
@router.get("/api/pitcher_names", tags=["scouting"])
def get_pitchers_by_team(team: str):
    try:
        df_pitcher_info = pi.get_pitchers(team)
        return {"pitchers": df_pitcher_info[["pitcher", "pitcher_hand"]].to_dict(orient="records")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching pitcher names: {str(e)}")
    
@router.get("/api/pitcher_data", tags=["scouting"])
def get_data_by_pitcher(pitcher: str):
    try:
        pickoffs, pick_per = pi.get_stat_percentile(pitcher, "pickoffs")
        pitches, pitch_per = pi.get_stat_percentile(pitcher, "pitches")
        games, games_per = pi.get_stat_percentile(pitcher, "games_played")
        ppg, ppg_per = pi.get_stat_percentile(pitcher, "picks_per_game")
        return {"pickoffs": [pickoffs, pick_per],
                "pitches": [pitches, pitch_per],
                "games": [games, games_per],
                "ppg": [ppg, ppg_per]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching pitcher stats: {str(e)}")
    
@router.get("/api/pickoff_hist", tags=["scouting"])
def get_pickoff_graphs(pitcher: str):
    try:
        df_pitcher_counts = pi.get_pitcher_data(pitcher)
        df_pitchers = pi.get_all_pitcher_data()
        pick_buf = viz.get_pickoff_counts_hist(df_pitchers, df_pitcher_counts["pickoffs"], pitcher)
        return Response(content=pick_buf.getvalue(), media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching plots: {str(e)}")
@router.get("/api/pitch_hist", tags=["scouting"])
def get_pitch_graphs(pitcher: str):
    try:
        df_pitcher_counts = pi.get_pitcher_data(pitcher)
        df_pitchers = pi.get_all_pitcher_data()
        pick_buf = viz.get_pitch_counts_hist(df_pitchers, df_pitcher_counts["pitches"], pitcher)
        return Response(content=pick_buf.getvalue(), media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching plots: {str(e)}")

@router.get("/api/games_hist", tags=["scouting"])
def get_games_graphs(pitcher: str):
    try:
        df_pitcher_counts = pi.get_pitcher_data(pitcher)
        df_pitchers = pi.get_all_pitcher_data()
        pick_buf = viz.get_games_played_hist(df_pitchers, df_pitcher_counts["games_played"], pitcher)
        return Response(content=pick_buf.getvalue(), media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching plots: {str(e)}")
    
@router.get("/api/ppg_hist", tags=["scouting"])
def get_ppg_graphs(pitcher: str):
    try:
        df_pitcher_counts = pi.get_pitcher_data(pitcher)
        df_pitchers = pi.get_all_pitcher_data()
        pick_buf = viz.get_ppg_hist(df_pitchers, df_pitcher_counts["picks_per_game"], pitcher)
        return Response(content=pick_buf.getvalue(), media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching plots: {str(e)}")
    
@router.get("/api/run_model", tags=["modeling"])
def run_model(outs: int, runs: int, pitcher_hand: int, batter_hand: int, base_dist: float, steal_score: float, home_team: int):
    try:
        columns = ['outs', 'run_diff', 'pitcher_hand', 'batter_hand', 'lead_distance', 'steal_score', 'is_home']
        model = joblib.load("database/rf_model.pkl")
        x_vals = [[outs, runs, pitcher_hand, batter_hand, base_dist, steal_score, home_team]]
        X = pd.DataFrame(x_vals, columns=columns)
        pred = model.predict_proba(X)[:, 1]
        percent_pred = round(pred[0]*100, 2)
        return {"prediction": f"{percent_pred}%"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error running model: {str(e)}")


        