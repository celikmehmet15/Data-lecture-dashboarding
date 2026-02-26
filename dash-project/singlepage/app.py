import dash
from dash import Dash, html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd


# Create app
app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


# Load data
emissions_df = pd.read_csv("emissions.csv")
emissions_df = emissions_df.query("year >= 1950")


# Create components
header = html.H1("CO2 emissions Dashboard", style={"textAlign": "center"})

country_dropdown = dcc.Dropdown(
    id="country_dropdown",
    options=[
        {"label": country, "value": country}
        for country in emissions_df["country"].unique()
    ],
    value="Turkey",
)


# Create callbacks
@callback(Output("country_co2", "figure"), Input("country_dropdown", "value"))
def update_country_co2(country):
    country_df = emissions_df[emissions_df["country"] == country]
    fig = px.line(country_df, x="year", y="co2", title=f"CO2 emissions in {country}")
    return fig


@callback(Output("country_co2_per_capita", "figure"), Input("country_dropdown", "value"))
def update_country_co2_pc(country):
    country_df = emissions_df[emissions_df["country"] == country]
    fig = px.line(
        country_df,
        x="year",
        y="co2_per_capita",
        title=f"CO2 per capita in {country}",
    )
    return fig

@callback(Output("country_co2_split", "figure"), Input("country_dropdown", "value"))
def update_country_co2_split(country):
    country_df = emissions_df[emissions_df["country"] == country].copy()

    # Bazı ülkelerde satırlar NaN olabiliyor; boş grafiği engeller
    country_df = country_df.dropna(subset=["oil_co2", "gas_co2", "coal_co2"], how="all")

    fig = px.line(
        country_df,
        x="year",
        y=["oil_co2", "gas_co2", "coal_co2"],
        title=f"CO2 emissions split in {country}",
    )
    return fig


# Define layout
app.layout = [
    dbc.Row(children=[dbc.Col(header, width=8), dbc.Col(country_dropdown, width=4)]),
    dbc.Row(
        children=[
            dbc.Col(dcc.Graph(id="country_co2"), width=8),
            dbc.Col(
                children=[
                    dcc.Graph(id="country_co2_split"),
                    dcc.Graph(id="country_co2_per_capita"),
                ],
                width=4,
            ),
        ]
    ),
]

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
