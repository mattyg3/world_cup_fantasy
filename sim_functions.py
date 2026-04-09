import random
from collections import defaultdict
import numpy as np

# -----------------------------
# CONFIG
# -----------------------------
# DRAW_PROB = 0.25  # probability of draw in group stage
# UPSET_FACTOR = 0.1 # added randomness for upsets (higher equals more upsets)

# -----------------------------
# TEAM STRUCTURE
# -----------------------------
class Team:
    def __init__(self, name, group, rating):
        self.name = name
        self.group = group
        self.rating = rating

# -----------------------------
# MATCH SIMULATION
# -----------------------------

def simulate_score(team_a, team_b, upset_factor):
    base_goals = 2.5

    diff = (team_a.rating - team_b.rating) / 60

    lambda_a = base_goals/2 + diff
    lambda_b = base_goals/2 - diff

    gap = abs(team_a.rating - team_b.rating) / 100
    shock_scale = upset_factor * (0.5 + 0.5 * (1 - gap))

    shock = np.random.normal(0, shock_scale)

    factor = np.exp(shock * 1.5)

    lambda_a = lambda_a * factor
    lambda_b = lambda_b / factor

    if lambda_a < 0:
        lambda_a = 0
    if lambda_b < 0:
        lambda_b = 0

    goals_a = np.random.poisson(lambda_a)
    goals_b = np.random.poisson(lambda_b)

    # --- Upset override ---
    if goals_a != goals_b:
        rating_diff = abs(team_a.rating - team_b.rating)
        # upset_prob = upset_factor * (1 - (rating_diff / 100)) * 1.5
        upset_prob = upset_factor * (0.2 + 0.8 * (1 - rating_diff / 100))

        if np.random.random() < upset_prob:
            return (goals_b, goals_a) if goals_a > goals_b else (goals_a, goals_b)


    return goals_a, goals_b

def simulate_knockout(team_a, team_b, upset_factor):
    g1, g2 = simulate_score(team_a, team_b, upset_factor)

    if g1 == g2:
        # penalties (coin flip)
        return random.choice([team_a, team_b])

    return team_a if g1 > g2 else team_b

# -----------------------------
# GROUP STAGE
# -----------------------------
def simulate_group(group_teams, upset_factor):
    table = {team.name: {"points": 0, "gd": 0, "team": team} for team in group_teams}

    for i in range(len(group_teams)):
        for j in range(i + 1, len(group_teams)):
            t1 = group_teams[i]
            t2 = group_teams[j]

            g1, g2 = simulate_score(t1, t2, upset_factor)

            if g1 == g2:
                table[t1.name]["points"] += 1
                table[t2.name]["points"] += 1
            elif g1 > g2:
                table[t1.name]["points"] += 3
            else:
                table[t2.name]["points"] += 3

            table[t1.name]["gd"] += (g1 - g2)
            table[t2.name]["gd"] += (g2 - g1)

    standings = sorted(
        table.values(),
        key=lambda x: (x["points"], x["gd"], x["team"].rating),
        reverse=True
    )

    return standings, table

# -----------------------------
# TOURNAMENT STRUCTURE
# -----------------------------
def get_group_results(groups, upset_factor):
    group_results = {}
    third_place_teams = []
    group_points = {}

    for group_name, teams in groups.items():
        standings, table = simulate_group(teams, upset_factor)
        group_results[group_name] = standings

        for team_name, stats in table.items():
            group_points[team_name] = stats["points"]

        third_place_teams.append(standings[2])

    return group_results, third_place_teams, group_points


def select_best_third(third_place_teams, n=8):
    ranked = sorted(
        third_place_teams,
        key=lambda x: (x["points"], x["gd"], x["team"].rating),
        reverse=True
    )
    return ranked[:n]

def bracket_builder(group_results, best_third):
    """
    Exact FIFA 2026 bracket based on provided image
    """

    G = group_results

    def get(group, pos):
        return G[group][pos]["team"]

    # --- Group winners / runners-up ---
    A1, A2 = get("A", 0), get("A", 1)
    B1, B2 = get("B", 0), get("B", 1)
    C1, C2 = get("C", 0), get("C", 1)
    D1, D2 = get("D", 0), get("D", 1)
    E1, E2 = get("E", 0), get("E", 1)
    F1, F2 = get("F", 0), get("F", 1)
    G1, G2 = get("G", 0), get("G", 1)
    H1, H2 = get("H", 0), get("H", 1)
    I1, I2 = get("I", 0), get("I", 1)
    J1, J2 = get("J", 0), get("J", 1)
    K1, K2 = get("K", 0), get("K", 1)
    L1, L2 = get("L", 0), get("L", 1)

    # --- Best 3rd place teams (ranked best → worst) ---
    T3 = [x["team"] for x in best_third]
    assert len(T3) == 8

    # --------------------------------------------------
    # ROUND OF 32
    # --------------------------------------------------

    return [
        # ===== LEFT BRACKET =====
        (E1, T3[0]),
        (I1, T3[1]),

        (A2, B2),
        (F1, C2),

        (K2, L2),
        (H1, J2),

        (D1, T3[2]),
        (G1, T3[3]),

        # ===== RIGHT BRACKET =====
        (C1, F2),
        (E2, I2),

        (A1, T3[4]),
        (L1, T3[5]),

        (J1, H2),
        (D2, G2),

        (B1, T3[6]),
        (K1, T3[7]),
    ]


# -----------------------------
# BRACKET HANDLING
# -----------------------------
def run_knockout_with_tracking(bracket_pairs, upset_factor):
    """
    Returns per-simulation advancement flags
    """

    advancement = defaultdict(lambda: {
        "R32": 0,
        "R16": 0,
        "QF": 0,
        "SF": 0,
        "Final": 0,
        "Champion": 0
    })

    current_round = bracket_pairs
    teams_in_round = [t for pair in current_round for t in pair]

    for t in teams_in_round:
        advancement[t.name]["R32"] = 1

    # R32 → R16
    winners = []
    for t1, t2 in current_round:
        winner = simulate_knockout(t1, t2, upset_factor)
        winners.append(winner)

    for t in winners:
        advancement[t.name]["R16"] = 1

    # R16 → QF
    current_round = [(winners[i], winners[i+1]) for i in range(0, len(winners), 2)]
    winners = []

    for t1, t2 in current_round:
        winner = simulate_knockout(t1, t2, upset_factor)
        winners.append(winner)

    for t in winners:
        advancement[t.name]["QF"] = 1

    # QF → SF
    current_round = [(winners[i], winners[i+1]) for i in range(0, len(winners), 2)]
    winners = []

    for t1, t2 in current_round:
        winner = simulate_knockout(t1, t2, upset_factor)
        winners.append(winner)

    for t in winners:
        advancement[t.name]["SF"] = 1

    # SF → Final
    current_round = [(winners[0], winners[1]), (winners[2], winners[3])]
    winners = []

    for t1, t2 in current_round:
        winner = simulate_knockout(t1, t2, upset_factor)
        winners.append(winner)

    for t in winners:
        advancement[t.name]["Final"] = 1

    # Final → Champion
    champion = simulate_knockout(winners[0], winners[1], upset_factor)
    advancement[champion.name]["Champion"] = 1

    return advancement

# -----------------------------
# MAIN SIMULATION
# -----------------------------
def simulate_tournament(teams, bracket_builder, n_sims, upset_factor):

    groups = defaultdict(list)
    for t in teams:
        groups[t.group].append(t)

    advancement_counts = {
        t.name: {
            "R32": 0,
            "R16": 0,
            "QF": 0,
            "SF": 0,
            "Final": 0,
            "Champion": 0
        }
        for t in teams
    }

    fantasy_points_total = {t.name: 0 for t in teams}

    for _ in range(n_sims):

        group_results, third_place, group_points = get_group_results(groups, upset_factor)
        best_third = select_best_third(third_place, n=8)

        knockout_pairs = bracket_builder(group_results, best_third)

        advancement = run_knockout_with_tracking(knockout_pairs, upset_factor)

        for team in teams:
            name = team.name
            
            sim_points = 0
            if advancement[name]["R32"]:
                sim_points += group_points.get(name, 0)
            if advancement[name]["R16"]:
                sim_points += 7
            if advancement[name]["QF"]:
                sim_points += 8
            if advancement[name]["SF"]:
                sim_points += 9
            if advancement[name]["Final"]:
                sim_points += 10
            if advancement[name]["Champion"]:
                sim_points += 11

            fantasy_points_total[name] += sim_points

            # accumulate advancement probabilities
            for stage in advancement[name]:
                advancement_counts[name][stage] += advancement[name][stage]

    # Normalize
    probs = {}
    for team in teams:
        name = team.name
        probs[name] = {
            stage: advancement_counts[name][stage] / n_sims
            for stage in advancement_counts[name]
        }
        probs[name]["ExpectedPoints"] = fantasy_points_total[name] / n_sims

    return probs


def pretty_print_results(probs, sort_by="ExpectedPoints", decimals=3):
    # Sort teams
    sorted_teams = sorted(
        probs.items(),
        key=lambda x: x[1][sort_by],
        reverse=True
    )

    # Header
    header = f"{'Team':<35} {'R32':>6} {'':>4} {'R16':>6} {'':>4} {'QF':>6} {'':>4} {'SF':>6} {'':>4} {'Final':>7} {'':>4} {'Champ':>7} {'':>4} {'ExpPts':>8}"
    print(header)
    print("-" * len(header))

    # Rows
    for team, stats in sorted_teams:
        print(
            f"{team:<35} "
            f"{stats['R32']:.{decimals}f} "
            f"{'':>6}",
            f"{stats['R16']:.{decimals}f} "
            f"{'':>6}",
            f"{stats['QF']:.{decimals}f} "
            f"{'':>6}",
            f"{stats['SF']:.{decimals}f} "
            f"{'':>6}",
            f"{stats['Final']:.{decimals}f} "
            f"{'':>6}",
            f"{stats['Champion']:.{decimals}f} "
            f"{'':>6}",
            f"{stats['ExpectedPoints']:.{decimals}f}"
        )


def sum_expected_points(probs, team_list, avg=False):
    # Create uppercase lookup
    probs_upper = {k.upper(): v for k, v in probs.items()}

    team_list_upper = [team.upper() for team in team_list]

    total = sum(
        probs_upper[team]["ExpectedPoints"]
        for team in team_list_upper
        if team in probs_upper
    )

    if avg and len(team_list_upper) > 0:
        return total / len(team_list_upper)

    return total