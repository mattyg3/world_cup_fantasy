# ⚽ World Cup Fantasy Tool

A fast, configurable Monte Carlo simulation engine for modeling FIFA
World Cup tournaments and estimating fantasy outcomes. Built with a
probabilistic match model, ELO-based ratings, and a fully implemented
2026 tournament structure.

🚀 **Live App:**
https://worldcupfantasy-auagibnd8zmjhc7e4uixgu.streamlit.app/

------------------------------------------------------------------------

## 🧠 Overview

This tool simulates thousands of complete World Cup tournaments to
estimate:

-   📊 Expected fantasy points per team
-   🏆 Advancement probabilities (R32 → Champion)
-   🎯 Fantasy roster performance

It is designed for both **fantasy optimization** and **tournament
modeling experimentation**.

------------------------------------------------------------------------

## ⚙️ Simulation Model

### Rating System

Input ratings (1--99) are converted into an ELO-like scale:

    ELO = 1200 + (rating - 50) * 15

This enables smoother probability curves and more realistic matchups.

------------------------------------------------------------------------

### Match Outcome Model

Each match is simulated in two stages:

#### 1. Outcome Sampling

-   Win probability is computed using a logistic function
-   Draw probability decreases with rating difference
-   Probabilities are normalized to sum to 1

#### 2. Upset Factor

A configurable **upset factor** injects controlled randomness:

-   Low values → chalk (favorites dominate)
-   Medium values (\~0.1) → realistic tournaments
-   High values → chaos

------------------------------------------------------------------------

### Score Generation

Goals are generated using a Poisson process conditioned on the match
result:

-   Ensures statistical realism
-   Guarantees consistency with sampled outcome (win/draw/loss)

------------------------------------------------------------------------

### Knockouts

-   Same model as group stage
-   Draws resolved via **penalty shootout (coin flip)**

------------------------------------------------------------------------

## 🏆 Tournament Format (2026)

-   12 groups (4 teams each)
-   Top 2 + 8 best 3rd-place teams advance
-   Knockout rounds:
    -   Round of 32
    -   Round of 16
    -   Quarterfinals
    -   Semifinals
    -   Final

------------------------------------------------------------------------

## 💰 Fantasy Scoring

  Stage           Points
  --------------- ---------------------------------------
 - Group Stage     Points earned (W=3, D=1) if advancing
 - Round of 16     +7
 - Quarterfinals   +8
 - Semifinals      +9
 - Final           +10
 - Champion        +11

------------------------------------------------------------------------

## 📦 Features

-   🔁 Monte Carlo simulation (100 → 100,000 runs)
-   🎚 Adjustable upset factor
-   📈 Advancement probabilities for every team
-   🧮 Expected fantasy points calculation
-   📊 Streamlit dashboard with visualizations
-   📁 CSV upload/download for custom ratings
-   🧩 Modular simulation engine

------------------------------------------------------------------------

## 🗂 Project Structure

    world_cup_fantasy_tool/
    ├── app.py              # Streamlit UI
    ├── sim_functions.py    # Simulation engine
    ├── fantasy_teams.py    # Fantasy rosters
    ├── team_ratings.csv    # Default ratings
    └── requirements.txt    # Dependencies

------------------------------------------------------------------------

## 🚀 Running Locally

    git clone https://github.com/mattyg3/world_cup_fantasy_tool.git
    cd world_cup_fantasy_tool
    pip install -r requirements.txt
    streamlit run app.py

------------------------------------------------------------------------

## 🔧 Customization

### Team Ratings

Edit or upload a CSV:

    Team,Group,Rating
    Brazil,A,85
    France,B,84

------------------------------------------------------------------------

### Fantasy Teams

Define rosters in `fantasy_teams.py`:

    fantasy_teams = {
        "Alice": ["Brazil", "France", "Germany"],
        "Bob": ["Argentina", "England", "Spain"],
    }

------------------------------------------------------------------------

## 🧪 Calibration

The engine tracks internal metrics for tuning:

-   `total_goals` → goal distribution
-   `match_draws` → draw rate
-   `upset_rate` → underdog win frequency

Useful for refining realism and parameter tuning.

------------------------------------------------------------------------

## 🛠 Tech Stack

-   Streamlit
-   NumPy
-   Pandas

------------------------------------------------------------------------

## 📄 License

MIT
