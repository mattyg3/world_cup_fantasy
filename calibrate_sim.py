from sim_functions import *
# from fantasy_teams import fantasy_teams
import pandas as pd
n_sims = 20000
upset_factor=0.1

teams_pdf = pd.read_csv('team_ratings.csv')
teams_pdf = teams_pdf.sort_values(by='Rating', ascending=False)

teams = []
for i, row in teams_pdf.iterrows():
    teams.append(Team(row['Team'], row['Group'], row['Rating']))

results = simulate_tournament(teams, bracket_builder, n_sims=n_sims, upset_factor=upset_factor)

# print(results)
print(f"AVG GOALS: {round(sum(total_goals) / len(total_goals), 2)}")
print(f"DRAW RATE: {round(sum(match_draws) / len(match_draws), 2)}")
print(f"UPSET RATE: {round(sum(upset_rate) / len(upset_rate), 2)}")