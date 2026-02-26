import dash
from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

# Register page
dash.register_page(__name__)

# Load data
emissions_df = pd.read_csv("emissions.csv")
emissions_df = emissions_df.query("year >= 1950")

# ---- Components ----
header = html.H1("Page with a dropdown and a map", style={"textAlign": "center"})

countries = sorted(emissions_df["country"].dropna().unique())

country_dropdown = dcc.Dropdown(
    id="withamap-country-dropdown",
    options=[{"label": c, "value": c} for c in countries],
    value="Turkey",
    clearable=False,
)

world_map = dcc.Graph(
    id="world_map",
    figure=px.choropleth(
        emissions_df[~emissions_df.iso_code.isna()].query("year == 2022"),
        locations="iso_code",
        color="co2_per_capita",
        title="CO2 emissions per capita (2022)",
    ),
)

regions_bar = dcc.Graph(
    id="regions_bar",
    figure=px.bar(
        emissions_df[
            emissions_df.country.isin(
                ["Africa", "Asia", "Europe", "North America", "Oceania", "South America"]
            )
        ]
        .query("year == 2022")
        .sort_values("co2_per_capita"),
        y="country",
        x="co2_per_capita",
        title="CO2 emissions per capita by region (2022)",
    ),
)

# ---- Callbacks ----
@callback(Output("country_co2", "figure"), Input("withamap-country-dropdown", "value"))
def update_country_co2(country):
    country_df = emissions_df[emissions_df["country"] == country]
    fig = px.line(country_df, x="year", y="co2", title=f"CO2 emissions in {country}")
    return fig


@callback(
    Output("country_co2_split", "figure"),
    Input("withamap-country-dropdown", "value"),
)
def update_country_co2_split(country):
    country_df = emissions_df[emissions_df["country"] == country].copy()
    country_df = country_df.dropna(subset=["oil_co2", "gas_co2", "coal_co2"], how="all")

    fig = px.line(
        country_df,
        x="year",
        y=["oil_co2", "gas_co2", "coal_co2"],
        title=f"CO2 emissions split in {country}",
    )
    return fig


# ---- Layout ----
layout = dbc.Container(
    [
        dbc.Row(children=[dbc.Col(header, width=8), dbc.Col(country_dropdown, width=4)]),
        dbc.Row(
            children=[
                dbc.Col(dcc.Graph(id="country_co2"), width=8),
                dbc.Col(dcc.Graph(id="country_co2_split"), width=4),
            ]
        ),
        dbc.Row(children=[dbc.Col(regions_bar, width=4), dbc.Col(world_map, width=8)]),
    ],
    fluid=True,
    className="p-4",
)
