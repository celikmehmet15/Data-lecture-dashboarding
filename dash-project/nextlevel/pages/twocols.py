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

countries = sorted(emissions_df["country"].dropna().unique())

layout = dbc.Container(
    [
        html.H1("Two columns", style={"textAlign": "center"}),

        dcc.Dropdown(
            id="country-dropdown-twocols",
            options=[{"label": c, "value": c} for c in countries],
            value="Turkey",
            clearable=False,
        ),

        dbc.Row(
            [
                dbc.Col(dcc.Graph(id="twocols-total-co2"), width=8),
                dbc.Col(dcc.Graph(id="twocols-split-co2"), width=4),
            ],
            className="mt-3",
        ),
    ],
    fluid=True,
    className="p-4",
)

@callback(
    Output("twocols-total-co2", "figure"),
    Output("twocols-split-co2", "figure"),
    Input("country-dropdown-twocols", "value"),
)
def update_twocols(country):
    country_df = emissions_df[emissions_df["country"] == country].copy()

    fig_total = px.line(
        country_df,
        x="year",
        y="co2",
        title=f"CO2 emissions in {country}",
    )

    # NaN olan yıllarda tamamen boş kalmasın
    df_split = country_df.dropna(subset=["oil_co2", "gas_co2", "coal_co2"], how="all")

    fig_split = px.line(
        df_split,
        x="year",
        y=["oil_co2", "gas_co2", "coal_co2"],
        title=f"CO2 split in {country}",
    )

    return fig_total, fig_split
