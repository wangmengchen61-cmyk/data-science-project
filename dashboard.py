# -*- coding: utf-8 -*-
"""
Automobile Sales Statistics Dashboard (Dash / Plotly)
=====================================================
Interactive dashboard for the Automobile Sales dataset (1980-2023).
Two report modes:
  1. Recession Period Statistics
  2. Yearly Statistics (per selected year)

Dataset source: IBM Developer Skills Network (public open dataset).

Run:
    pip install -r requirements.txt
    python dashboard.py
Then open http://127.0.0.1:8050 in your browser.
"""

import os

import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "automobile-sales.csv")

# Load the data
data = pd.read_csv(DATA_PATH)

# Initialize the Dash app
app = Dash(__name__)
app.title = "Automobile Sales Statistics Dashboard"

# Dropdown options
dropdown_options = [
    {"label": "Yearly Statistics", "value": "Yearly Statistics"},
    {"label": "Recession Period Statistics", "value": "Recession Period Statistics"},
]
year_list = [i for i in range(1980, 2024, 1)]

# Layout
app.layout = html.Div([
    html.H1("Automobile Sales Statistics Dashboard",
            style={"textAlign": "center", "color": "#503D36", "font-size": "24px"}),
    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id="dropdown-statistics",
            options=dropdown_options,
            value="Select Statistics",
            placeholder="Select a report type",
            style={"width": "80%", "padding": "3px",
                   "font-size": "20px", "text-align-last": "center"},
        ),
    ]),
    html.Div(dcc.Dropdown(
        id="select-year",
        options=[{"label": i, "value": i} for i in year_list],
        value="Select-year",
        placeholder="Select-year",
    )),
    html.Div([
        html.Div(id="output-container", className="chart-grid",
                 style={"display": "flex"}),
    ]),
])


@app.callback(
    Output(component_id="select-year", component_property="disabled"),
    Input(component_id="dropdown-statistics", component_property="value"),
)
def update_input_container(selected_statistics):
    """Enable year dropdown only for Yearly Statistics."""
    return selected_statistics != "Yearly Statistics"


@app.callback(
    Output(component_id="output-container", component_property="children"),
    [Input(component_id="dropdown-statistics", component_property="value"),
     Input(component_id="select-year", component_property="value")],
)
def update_output_container(selected_statistics, input_year):
    if selected_statistics == "Recession Period Statistics":
        recession_data = data[data["Recession"] == 1]

        # Plot 1: sales fluctuation over recession periods (year-wise)
        yearly_rec = recession_data.groupby("Year")["Automobile_Sales"].mean().reset_index()
        r_chart1 = dcc.Graph(
            figure=px.line(yearly_rec, x="Year", y="Automobile_Sales",
                           title="Average Automobile Sales Fluctuation over Recession Period"))

        # Plot 2: average number of vehicles sold by vehicle type
        average_sales = (recession_data.groupby("Vehicle_Type")["Automobile_Sales"]
                         .mean().reset_index())
        r_chart2 = dcc.Graph(
            figure=px.bar(average_sales, x="Vehicle_Type", y="Automobile_Sales",
                          title="Average Number of Vehicles Sold by Vehicle Type"))

        # Plot 3: total expenditure share by vehicle type during recessions
        exp_rec = (recession_data.groupby("Vehicle_Type")["Advertising_Expenditure"]
                   .sum().reset_index())
        r_chart3 = dcc.Graph(
            figure=px.pie(exp_rec, values="Advertising_Expenditure",
                          names="Vehicle_Type",
                          title="Total Expenditure Share by Vehicle Type During Recessions"))

        # Plot 4: effect of unemployment rate on vehicle type and sales
        unemp_data = (recession_data
                      .groupby(["unemployment_rate", "Vehicle_Type"])["Automobile_Sales"]
                      .mean().reset_index())
        r_chart4 = dcc.Graph(
            figure=px.bar(unemp_data, x="unemployment_rate", y="Automobile_Sales",
                          color="Vehicle_Type",
                          labels={"unemployment_rate": "Unemployment Rate",
                                  "Automobile_Sales": "Average Automobile Sales"},
                          title="Effect of Unemployment Rate on Vehicle Type and Sales"))

        return [
            html.Div(className="chart-item",
                     children=[html.Div(children=r_chart1), html.Div(children=r_chart2)],
                     style={"display": "flex"}),
            html.Div(className="chart-item",
                     children=[html.Div(children=r_chart3), html.Div(children=r_chart4)],
                     style={"display": "flex"}),
        ]

    if input_year and selected_statistics == "Yearly Statistics":
        yearly_data = data[data["Year"] == input_year]

        # Plot 1: yearly automobile sales (whole period)
        yas = data.groupby("Year")["Automobile_Sales"].mean().reset_index()
        y_chart1 = dcc.Graph(
            figure=px.line(yas, x="Year", y="Automobile_Sales",
                           title="Yearly Automobile Sales"))

        # Plot 2: total monthly automobile sales
        mas = yearly_data.groupby("Month")["Automobile_Sales"].sum().reset_index()
        month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                       "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        mas["Month"] = pd.Categorical(mas["Month"], categories=month_order, ordered=True)
        mas = mas.sort_values("Month")
        y_chart2 = dcc.Graph(
            figure=px.line(mas, x="Month", y="Automobile_Sales",
                           title="Total Monthly Automobile Sales"))

        # Plot 3: average number of vehicles sold by type in the given year
        avr_vdata = (yearly_data.groupby("Vehicle_Type")["Automobile_Sales"]
                     .mean().reset_index())
        y_chart3 = dcc.Graph(
            figure=px.bar(avr_vdata, x="Vehicle_Type", y="Automobile_Sales",
                          title=f"Average Vehicles Sold by Vehicle Type in {input_year}"))

        # Plot 4: total advertisement expenditure by vehicle type
        exp_data = (yearly_data.groupby("Vehicle_Type")["Advertising_Expenditure"]
                    .sum().reset_index())
        y_chart4 = dcc.Graph(
            figure=px.pie(exp_data, values="Advertising_Expenditure",
                          names="Vehicle_Type",
                          title="Total Advertisement Expenditure by Vehicle Type"))

        return [
            html.Div(className="chart-item",
                     children=[html.Div(children=y_chart1), html.Div(children=y_chart2)],
                     style={"display": "flex"}),
            html.Div(className="chart-item",
                     children=[html.Div(children=y_chart3), html.Div(children=y_chart4)],
                     style={"display": "flex"}),
        ]
    return None


if __name__ == "__main__":
    app.run(debug=True)
