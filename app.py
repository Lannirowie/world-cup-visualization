import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px

# Load data
df = pd.read_csv("world_cup_finals.csv", dtype={"Year": str})

# Drop any rows with missing values
df.dropna(subset=["Winner", "Year"], inplace=True)

# Normalize types
df["Winner"] = df["Winner"].astype(str)
df["Year"] = df["Year"].astype(str)

# Calculate win counts
win_counts = df["Winner"].value_counts().reset_index()
win_counts.columns = ["Country", "Wins"]

# Initialize app
app = dash.Dash(__name__)
app.title = "FIFA World Cup Dashboard"

# Layout
app.layout = html.Div([
    html.H1("FIFA World Cup Dashboard", style={'textAlign': 'center'}),

    dcc.Graph(id="choropleth-map"),

    html.Label("Select a Country:"),
    dcc.Dropdown(
        options=[{"label": c, "value": c} for c in sorted(df["Winner"].unique())],
        id="country-dropdown"
    ),
    html.Div(id="win-output"),

    html.Label("Select a Year:"),
    dcc.Dropdown(
        options=[{"label": y, "value": y} for y in sorted(df["Year"].unique())],
        id="year-dropdown"
    ),
    html.Div(id="year-output")
])

# Callbacks
@app.callback(
    Output("choropleth-map", "figure"),
    Input("country-dropdown", "value")
)
def update_map(selected_country):
    fig = px.choropleth(win_counts,
                        locations="Country",
                        locationmode="country names",
                        color="Wins",
                        title="Countries that have won the World Cup",
                        color_continuous_scale="Viridis")
    return fig


@app.callback(
    Output("win-output", "children"),
    Input("country-dropdown", "value")
)
def display_wins(country):
    if country:
        wins = df[df["Winner"] == country].shape[0]
        return f"{country} has won the World Cup {wins} time(s)."
    return ""


@app.callback(
    Output("year-output", "children"),
    Input("year-dropdown", "value")
)
def display_final(year):
    if year:
        match = df[df["Year"] == year]
        if not match.empty:
            winner = match["Winner"].values[0]
            runner = match["RunnerUp"].values[0]
            return f"In {year}, {winner} won and {runner} was the runner-up."
    return ""

# Run server
if __name__ == "__main__":
    app.run(debug=True)
