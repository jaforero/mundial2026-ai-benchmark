# ChatGPT_v7_top_goleadores.py
import math
import pandas as pd

def poisson_tail(mu, k_min):
    return 1 - sum(math.exp(-mu) * (mu ** k) / math.factorial(k) for k in range(k_min))

def effective_minutes_share(start_probability, minutes_start, minutes_sub):
    return start_probability * (minutes_start / 90) + (1 - start_probability) * (minutes_sub / 90)

def expected_goals_player(
    expected_matches_team,
    team_goals_per_match,
    player_xg_share,
    effective_minutes,
    penalty_adjustment,
    current_form,
    medical_availability,
    match_sharpness,
    rotation_adjustment,
    opponent_adjustment
):
    return (
        expected_matches_team
        * team_goals_per_match
        * player_xg_share
        * effective_minutes
        * penalty_adjustment
        * current_form
        * medical_availability
        * match_sharpness
        * rotation_adjustment
        * opponent_adjustment
    )

def add_goal_probabilities(df, goals_col="Goles esperados v7-G"):
    df = df.copy()
    df["P(4+ goles)"] = df[goals_col].apply(lambda x: round(poisson_tail(x, 4) * 100, 1))
    df["P(5+ goles)"] = df[goals_col].apply(lambda x: round(poisson_tail(x, 5) * 100, 1))
    return df

# Uso:
# scorers = pd.read_csv("input_goleadores_base.csv")
# scorers = add_goal_probabilities(scorers, "Goles esperados v7-G")
# scorers.to_csv("ChatGPT_Goleadores_Fase_7.csv", index=False)
