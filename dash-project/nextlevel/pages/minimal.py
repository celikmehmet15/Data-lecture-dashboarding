import dash
from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

dash.register_page(__name__)

emissions_df = pd.read_csv("emissions.csv")
emissions_df = emissions_df.query("year >= 1950")

layout = dbc.Container(
    [
        html.H1("A very minimal page", style={"textAlign": "center"}),

        dcc.Dropdown(
            id="country-dropdown-min",
            options=[{"label": c, "value": c} for c in sorted(emissions_df["country"].dropna().unique())],
            value="Turkey",
            clearable=False,
        ),

        dcc.Graph(id="country-co2"),
    ],
    className="p-4",
)

@callback(Output("country-co2", "figure"), Input("country-dropdown-min", "value"))
def update_country(country):
    country_df = emissions_df[emissions_df["country"] == country]
    fig = px.line(country_df, x="year", y="co2", title=f"CO2 emissions in {country}")
    return fig
