# ⚽ World Cup Fantasy Tool

A Monte Carlo simulation tool for scoring World Cup fantasy tournaments. Run thousands of simulated tournaments to estimate expected fantasy points for each player's team, based on real team ratings and a fully modeled FIFA 2026 bracket.

**Live App:** [worldcupfantasytool on Streamlit](https://worldcupfantasy-auagibnd8zmjhc7e4uixgu.streamlit.app/)

---

## How It Works

The simulator runs N complete World Cup tournaments (default: 20,000) and tracks how far each national team advances. Fantasy player scores are then calculated by summing the expected points earned by each team in their roster across all simulations.

**Point values per round:**
| Round | Points |
|---|---|
| Group Stage | Points = group stage points earned (W=3, D=1) if team advances to Round of 32 |
| Round of 16 | +7 |
| Quarterfinals | +8 |
| Semifinals | +9 |
| Final | +10 |
| Champion | +11 |

### Match Simulation

Each match uses a Poisson goal model where expected goals for each team are derived from their rating differential. An **upset factor** adds a normally-distributed shock to the expected goals, making lower-rated teams more likely to win than pure ratings would suggest. Knockout matches that end level go to a simulated penalty shootout (coin flip).

### Tournament Structure

The bracket follows the **exact FIFA 2026 format**: 12 groups of 4, a Round of 32 (including the 8 best third-place finishers), then Round of 16, Quarterfinals, Semifinals, and Final.

---

## Features

- **Monte Carlo simulation** — run 100 to 100,000 tournaments
- **Adjustable upset factor** — dial up chaos or play it chalk
- **Fantasy leaderboard** — expected score per player, visualized as a bar chart
- **Per-team breakdown** — advancement probabilities for every round
- **Custom ratings** — upload your own `team_ratings.csv` to override defaults
- **CSV export** — download the current ratings data at any time

---

## Project Structure

```
world_cup_fantasy_tool/
├── app.py              # Streamlit UI
├── sim_functions.py    # Simulation engine (match model, bracket logic, scoring)
├── fantasy_teams.py    # Fantasy player rosters
├── team_ratings.csv    # Default team ratings
└── requirements.txt    # Python dependencies
```

---

## Running Locally

**1. Clone the repo**
```bash
git clone https://github.com/mattyg3/world_cup_fantasy_tool.git
cd world_cup_fantasy_tool
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Run the app**
```bash
streamlit run app.py
```

---

## Customization

### Team Ratings

The default `team_ratings.csv` contains a `Team`, `Group`, and `Rating` column. You can edit ratings and re-upload the CSV in the app sidebar to reflect your own power rankings.

```csv
Team,Group,Rating
Brazil,A,85
France,B,84
...
```

### Fantasy Rosters

Edit `fantasy_teams.py` to define player names and their drafted national teams:

```python
fantasy_teams = {
    "Alice": ["Brazil", "France", "Germany", ...],
    "Bob":   ["Argentina", "England", "Spain", ...],
}
```

---

## Tech Stack

- [Streamlit](https://streamlit.io/) — web app framework
- [NumPy](https://numpy.org/) — Poisson goal modeling and upset shocks
- [Pandas](https://pandas.pydata.org/) — data handling and display

---

## License

MIT

