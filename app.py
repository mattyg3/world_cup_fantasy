import streamlit as st
from sim_functions import *
from fantasy_teams import fantasy_teams
import pandas as pd

@st.cache_data
def load_default_data():
    teams_pdf = pd.read_csv('team_ratings.csv')
    teams_pdf = teams_pdf.sort_values(by='Rating', ascending=False)
    # teams_pdf['rank'] = range(1, len(teams_pdf) + 1)
    return teams_pdf

teams_pdf = load_default_data()

if "teams" not in st.session_state:
    st.session_state.df = teams_pdf.copy()

uploaded_file = st.file_uploader("Upload edited CSV", type="csv")

if uploaded_file is not None:
    teams_pdf = pd.read_csv(uploaded_file)
    teams_pdf = teams_pdf.sort_values(by='Rating', ascending=False)
    # teams_pdf['rank'] = range(1, len(teams_pdf) + 1)
    st.session_state.df = teams_pdf
    st.success("Uploaded file is now active!")

st.title("⚽ World Cup Fantasy: Monte Carlo Simulator")

# -----------------------------
# INPUTS
# -----------------------------
st.sidebar.header("⚙️ Simulation Settings")

# n_sims = st.sidebar.slider("Number of Simulations", 100, 100000, 20000)
# upset_factor = st.sidebar.slider("Upset Factor", 0.0, 0.99, 0.05)
n_sims = st.slider("Number of Simulations", 100, 100000, 20000)
upset_factor = st.slider("Upset Factor", 0.0, 0.99, 0.05)

# -----------------------------
# RUN SIMULATION
# -----------------------------
if st.button("Run Simulation"):
    with st.spinner("Simulating tournament..."):
        teams = []
        for i, row in st.session_state.df.iterrows():
            teams.append(Team(row['Team'], row['Group'], row['Rating']))

        results = simulate_tournament(teams, bracket_builder, n_sims=n_sims, upset_factor=upset_factor)

    st.success("Done!")

    # Convert to table
    df = pd.DataFrame.from_dict(results, orient="index")
    df = df.sort_values("ExpectedPoints", ascending=False)
    # df['rank_results'] = range(1, len(df) + 1)
    df = df.reset_index(names='Team')

    player = []
    score= []
    for key, value in fantasy_teams.items():
        expected_score = sum_expected_points(results, value, avg=False)
        player.append(key)
        score.append(expected_score)

    pdf = pd.DataFrame({'Player': player, 'Expected Score': score})






    st.subheader("📊 Simulated Fantasy Results")
    chart_df = pdf.set_index("Player")["Expected Score"]
    st.bar_chart(chart_df)

    # st.subheader("🗒️ Fantasy Results")
    pdf = pdf.sort_values(by=['Expected Score'], ascending=False)
    pdf["Expected Score"] = round(pdf["Expected Score"], 2).astype(str)
    styled_pdf = pdf.style.set_properties(**{"text-align": "left"})
    st.dataframe(styled_pdf, hide_index=True)

    fantasy_df = pd.DataFrame(fantasy_teams)
    st.subheader("🗒️ Fantasy Teams")
    st.dataframe(fantasy_df, hide_index=True)





    st.subheader("🗒️ Individual Team Results")
    df = df[['Team', 'R32', 'R16', 'QF', 'SF', 'Final', 'Champion', 'ExpectedPoints']]
    styled_df = df.style.set_properties(**{"text-align": "left"})
    st.dataframe(styled_df, hide_index=True)

    # Expected points
    st.subheader("📊 Individual Team Expected Points")
    st.bar_chart(df,x="Team", y="ExpectedPoints")

    # st.subheader("📉 Outcome Distribution")

    # selected_team = st.selectbox("Select Team", df["Team"])
    # # simulate distribution
    # points_dist = []

    # for _ in range(5000):
    #     res = simulate_tournament(teams, bracket_builder, n_sims=1, upset_factor=upset_factor)
    #     points_dist.append(res[selected_team]["ExpectedPoints"])

    # hist_df = pd.DataFrame(points_dist, columns=["Points"])
    # st.bar_chart(hist_df)

    # st.subheader("🧗 Path Difficulty")

    # path_df = df.merge(
    #     st.session_state.df[['Team', 'Rating']],
    #     on='Team'
    # )

    # # proxy: lower advancement vs rating = harder path
    # path_df["Difficulty"] = path_df["Rating"] * (1 - path_df["QF"])

    # st.bar_chart(path_df.sort_values("Difficulty", ascending=False), #.head(15)
    #             x="Team", y="Difficulty")

    # st.subheader("💎 Value Picks (Points vs Rating)")

    # value_df = df.merge(
    #     st.session_state.df[['Team', 'Rating']],
    #     on='Team'
    # )

    # value_df["Value"] = value_df["ExpectedPoints"] / value_df["Rating"]

    # st.scatter_chart(
    #     value_df,
    #     x="Rating",
    #     y="ExpectedPoints"
    # )


    # st.subheader("💎 Value Picks (Points vs Rating)")

    # value_df = df.merge(
    #     st.session_state.df[['Team', 'Rating']],
    #     on='Team'
    # )

    # value_df["Value"] = value_df["ExpectedPoints"] / value_df["Rating"]

    # chart = alt.Chart(value_df).mark_circle(size=80).encode(
    #     x=alt.X("Rating", title="Rating"),
    #     y=alt.Y("ExpectedPoints", title="Expected Points"),
    #     tooltip=["Team", "Rating", "ExpectedPoints", "Value"]
    # )

    # text = chart.mark_text(
    #     align='left',
    #     baseline='middle',
    #     dx=5
    # ).encode(
    #     text='Team'
    # )

    # st.altair_chart(chart + text, use_container_width=True)






    st.subheader("Current Rating Data (Use Ratings between 1-99)")
    df_csv = st.session_state.df.sort_values(by=['Rating'], ascending=False)
    df_csv = df_csv[['Team', 'Rating', 'Group']]
    df_csv["Rating"] = df_csv["Rating"].astype(str)
    styled_df_csv = df_csv.style.set_properties(**{"text-align": "left"})
    st.dataframe(styled_df_csv, hide_index=True)

    csv = st.session_state.df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Current CSV",
        data=csv,
        file_name="editable_data.csv",
        mime="text/csv"
    )